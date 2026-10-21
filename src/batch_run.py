"""Batch runner: evaluates all strategies and prints a comparison table.

Usage: python3 src/batch_run.py [--universe sp500_top|etfs|large_liquid]
"""

import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.run_experiment import run_strategy, STRATEGIES, UNIVERSES
from src import jsonio

parser = argparse.ArgumentParser()
parser.add_argument("--universe", default="sp500_top", choices=list(UNIVERSES.keys()))
args = parser.parse_args()

UNIVERSE = args.universe
universe = UNIVERSES[UNIVERSE]

print(f"{'strategy':<18} {'IS_Sharpe':>9} {'OOS_Sharpe':>10} {'OOS_AnnRet':>10} {'OOS_MaxDD':>10} {'PosFolds':>9} {'BM_Sharpe':>9}")
print("-" * 85)
results = {}
for name in STRATEGIES:
    try:
        r = run_strategy(name, universe)
        results[name] = r
        is_s = r["in_sample"]["sharpe"]
        bm_s = r["benchmark"]["sharpe"]
        sharps = [f["sharpe"] for f in r["oos_folds"]]
        oos_s = float(np.mean(sharps))
        oos_ret = float(np.mean([f["annual_return"] for f in r["oos_folds"]]))
        oos_dd = float(np.mean([f["max_drawdown"] for f in r["oos_folds"]]))
        pos = sum(1 for s in sharps if s > 0)
        print(f"{name:<18} {is_s:>9.3f} {oos_s:>10.3f} {oos_ret:>10.3f} {oos_dd:>10.3f} {pos:>4}/{len(sharps):<4} {bm_s:>9.3f}")
        out = os.path.join("experiments", f"{name}_{UNIVERSE}.json")
        with open(out, "w") as f:
            jsonio.dump(r, f, indent=2, default=str)
    except Exception as e:
        print(f"{name:<18} ERROR: {e}")

# Save summary
summary = {}
for name, r in results.items():
    sharps = [f["sharpe"] for f in r["oos_folds"]]
    summary[name] = {
        "is_sharpe": r["in_sample"]["sharpe"],
        "oos_mean_sharpe": float(np.mean(sharps)),
        "oos_sharpe_std": float(np.std(sharps)),
        "oos_mean_ann_return": float(np.mean([f["annual_return"] for f in r["oos_folds"]])),
        "oos_mean_max_dd": float(np.mean([f["max_drawdown"] for f in r["oos_folds"]])),
        "pos_folds": int(sum(1 for s in sharps if s > 0)),
        "n_folds": len(sharps),
        "bm_sharpe": r["benchmark"]["sharpe"],
    }
with open(os.path.join("experiments", "summary.json"), "w") as f:
    jsonio.dump(summary, f, indent=2)
print("\nSaved experiments/summary.json")