"""Run placebo validation across all strategies and write results to experiments/.

Usage: python3 src/validate.py [--universe sp500_top|etfs|large_liquid]
"""

import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import data, backtest, validation, strategies
from src.run_experiment import UNIVERSES

STRATEGIES = {
    "momentum": strategies.momentum,
    "momentum_6m": strategies.max_momentum,
    "reversal": strategies.reversal,
    "value": strategies.value,
    "short_reversal": strategies.short_reversal,
    "low_vol": strategies.low_vol,
    "quality": strategies.quality,
    "mean_reversion_5": strategies.mean_reversion_5,
}

parser = argparse.ArgumentParser()
parser.add_argument("--universe", default="sp500_top", choices=list(UNIVERSES.keys()))
args = parser.parse_args()

UNIVERSE = UNIVERSES[args.universe]

df = data.download(UNIVERSE, start="2014-01-01")
close = data.get_panel(df, "Close").dropna(how="all")

print("Building placebo distribution (50 random sims)...")
placebo = validation.placebo_distribution(close, n_sim=50)
print("Placebo: mean Sharpe=%.3f, std=%.3f, %%positive=%.1f%%" % (
    placebo["mean_sharpe"], placebo["std_sharpe"], placebo["pct_positive"] * 100
))

summary = {"placebo": placebo, "strategies": {}}
for name, fn in STRATEGIES.items():
    signal = fn(close)
    weights = backtest.equal_weight_weights(signal, long_only=True)
    rets = backtest.portfolio_returns(weights, close, close)
    m = backtest.metrics(rets["net"])
    # walk-forward OOS sharps
    splits = backtest.walk_forward_splits(len(close), 504, 63, 63)
    oos_sharpes = []
    for tr_s, tr_e, te_s, te_e in splits:
        test_idx = close.index[te_s:te_e]
        test_rets = rets.loc[rets.index.intersection(test_idx)]
        oos_sharpes.append(backtest.metrics(test_rets["net"]).get("sharpe", 0.0))

    comp = validation.compare_to_placebo(oos_sharpes, placebo["mean_sharpe"], placebo["std_sharpe"])
    acf = validation.autocorrelation_test(rets["net"])
    summary["strategies"][name] = {
        "is_sharpe": m.get("sharpe"),
        "is_ann_return": m.get("annual_return"),
        "is_max_dd": m.get("max_drawdown"),
        "oos_mean_sharpe": comp.get("mean_sharpe"),
        "oos_sharpe_std": float(np.std(oos_sharpes)),
        "oos_z_score": comp.get("z_score"),
        "oos_pos_folds": int(sum(1 for s in oos_sharpes if s > 0)),
        "oos_n_folds": len(oos_sharpes),
        "acf_lag1": acf["acf"][0],
        "t_stat": validation.t_stat(m.get("sharpe", 0.0), m.get("n_days", 252)),
    }
    print(f"{name:<18} IS_Sharpe={m.get('sharpe',0):.3f} OOS_Sharpe={comp.get('mean_sharpe',0):.3f} z={comp.get('z_score',0):.2f} pos={summary['strategies'][name]['oos_pos_folds']}/{len(oos_sharpes)}")

with open(os.path.join("experiments", "validation_summary.json"), "w") as f:
    json.dump(summary, f, indent=2, default=str)
print("\nSaved experiments/validation_summary.json")