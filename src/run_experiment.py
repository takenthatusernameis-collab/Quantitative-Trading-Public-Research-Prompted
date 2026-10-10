"""Experiment runner: evaluates a strategy via walk-forward and writes results.

Usage:
    python -m src.run_experiment momentum --universe SPY QQQ IWM VOO VGT XLK XLF XLE
"""

import argparse
import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import data, backtest, strategies

STRATEGIES = {
    "momentum": strategies.momentum,
    "momentum_6m": strategies.max_momentum,
    "reversal": strategies.reversal,
    "value": strategies.value,
    "short_reversal": strategies.short_reversal,
    "low_vol": strategies.low_vol,
    "quality": strategies.quality,
    "mean_reversion_5": strategies.mean_reversion_5,
    "random": None,  # placebo baseline
}

UNIVERSES = {
    "sp500_top": ["SPY", "QQQ", "IWM", "VOO", "VGT", "XLK", "XLF", "XLE", "XLV", "XLI"],
    "etfs": ["SPY", "QQQ", "IWM", "VOO", "VGT", "XLK", "XLF", "XLE", "GLD", "TLT"],
    "large_liquid": [
  "AAPL","ABBV","ABT","ACN","ADBE","ADI","ADM","ADP","ADSK","AEP",
  "AIG","ALL","AMAT","AMD","AMGN","AMT","AMZN","AVGO","AXP","BA",
  "BAC","BK","BKNG","BMY","BRK-B","BSX","C","CAT","CCI","CDNS",
  "CHTR","CI","CL","CMCSA","CME","COF","COP","COST","CRM","CSCO",
  "CSX","CVS","CVX","DE","DHR","DIS","DOW","DXCM","EMR","EOG",
  "EQIX","ETN","EXC","FDX","FIS","FTNT","GD","GE","GILD","GM",
  "GOOG","GOOGL","GS","HD","HON","IBM","ICE","INTC","INTU","ISRG",
  "JNJ","JPM","KDP","KHC","KLAC","KO","LIN","LLY","LMT","LOW",
  "LRCX","MA","MCD","MDLZ","MDT","META","MET","MMM","MO","MRK",
  "MS","MSFT","MU","NFLX","NKE","NOW","NVDA","ORCL","PCAR","PEP",
  "PFE","PG","PLD","PM","PNC","PYPL","QCOM","REGN","ROST","RTX",
  "SBUX","SCHW","SLB","SO","SPG","T","TGT","TJX","TMO","TMUS",
  "TSLA","TXN","UNH","UNP","UPS","USB","V","VZ","WBA","WFC",
  "WMT","XOM"
],}


def run_strategy(strategy_name: str, universe: list, train: int = 504, test: int = 63, step: int = 63,
                  tc_cost: float = 0.0005, slippage: float = 0.0002) -> dict:
    sig_fn = STRATEGIES[strategy_name]
    df = data.download(universe, start="2014-01-01")
    close = data.get_panel(df, "Close").copy()
    open_ = data.get_panel(df, "Open").copy()

    close = close.dropna(how="all")
    open_ = open_.reindex(close.index).fillna(close)

    if strategy_name == "random":
        rng = np.random.default_rng(42)
        signal = pd.DataFrame(
            rng.standard_normal(size=close.shape),
            index=close.index, columns=close.columns,
        )
    else:
        signal = sig_fn(close)
    weights = backtest.equal_weight_weights(signal, long_only=True)
    rets = backtest.portfolio_returns(weights, close, open_, tc_cost=tc_cost, slippage=slippage)
    turnover_avg = backtest.average_turnover(weights)

    # benchmark
    bm = data.get_benchmark("SPY", start="2014-01-01")
    bm_ret = bm["close"].pct_change().fillna(0.0)

    # align
    common = rets.index.intersection(bm_ret.index)
    rets = rets.loc[common]
    bm_ret = bm_ret.loc[common]

    strat_metrics = backtest.metrics(rets["net"])
    bm_metrics = backtest.metrics(bm_ret)

    # walk-forward
    splits = backtest.walk_forward_splits(len(close), train, test, step)
    oos_results = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        test_idx = close.index[te_s:te_e]
        test_rets = rets.loc[rets.index.intersection(test_idx)]
        m = backtest.metrics(test_rets["net"])
        m["fold"] = i
        oos_results.append(m)

    result = {
        "strategy": strategy_name,
        "universe": universe,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "in_sample": strat_metrics,
        "benchmark": bm_metrics,
        "oos_folds": oos_results,
        "n_folds": len(splits),
        "turnover_avg": turnover_avg,
        "costs": {"tc_cost": tc_cost, "slippage": slippage},
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("strategy", choices=list(STRATEGIES.keys()))
    parser.add_argument("--universe", default="sp500_top")
    parser.add_argument("--train", type=int, default=504)
    parser.add_argument("--test", type=int, default=63)
    parser.add_argument("--step", type=int, default=63)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    universe = UNIVERSES[args.universe]
    result = run_strategy(args.strategy, universe, args.train, args.test, args.step)

    out_path = args.out or os.path.join("experiments", f"{args.strategy}_{args.universe}.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()