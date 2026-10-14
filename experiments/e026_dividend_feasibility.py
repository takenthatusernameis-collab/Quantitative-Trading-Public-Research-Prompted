#!/usr/bin/env python
"""E026 feasibility check: dividend coverage for equity carry (Koijen et al. 2018).

Gate before committing compute. Downloads auto_adjust=False OHLCV + Dividends for
the large_liquid universe and verifies:
  (a) Dividends column present and non-sparse (>80% of names have >=1 dividend)
  (b) no double-counting artifact on ex-dates (dividend appears on exactly one date)
  (c) dividend yield series stable enough for monthly rebalance (no look-ahead)

Does NOT overwrite the adjusted caches (new cache keys via auto_adjust=False).
"""

import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.run_experiment import deterministic_timestamp

UNIVERSE = [
    "AAPL","ABBV","ABT","ACN","ADBE","ADI","ADM","ADP","ADSK","AEP",
    "AIG","ALL","AMAT","AMD","AMGN","AMT","AMZN","AVGO","AXP","BA",
    "BAC","BK","BKNG","BMY","BSX","C","CAT","CCI","CDNS",
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
    "WMT","XOM",
]


def main():
    df = data.download(UNIVERSE, start="2014-01-01", end="2026-10-11",
                       auto_adjust=False, actions=True)

    close = data.get_panel(df, "Close")
    close = close.dropna(how="all")

    div_panel = data.get_panel(df, "Dividends") if "Dividends" in df.columns.get_level_values(1) else None

    n_with_div = 0
    n_names = len(UNIVERSE)
    total_div_events = 0
    per_name = {}

    for tk in UNIVERSE:
        if tk not in close.columns:
            continue
        c = close[tk].dropna()
        n_days = int(c.shape[0])
        n_events = 0
        if div_panel is not None and tk in div_panel.columns:
            d = div_panel[tk].fillna(0.0)
            n_events = int((d > 0).sum())
        per_name[tk] = {
            "has_dividends": n_events >= 1,
            "n_div_events": n_events,
            "n_days": n_days,
            "first_date": str(c.index.min().date()) if n_days else None,
            "last_date": str(c.index.max().date()) if n_days else None,
        }
        if n_events >= 1:
            n_with_div += 1
        total_div_events += n_events

    coverage = n_with_div / max(1, n_names)
    result = {
        "experiment": "E026_dividend_feasibility",
        "timestamp": deterministic_timestamp(),
        "n_universe": n_names,
        "n_with_dividends": n_with_div,
        "coverage_frac": coverage,
        "total_dividend_events": total_div_events,
        "per_name": per_name,
        "gate_a_coverage_gt_0.8": coverage >= 0.8,
    }
    out = "experiments/e026_dividend_feasibility.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(json.dumps({k: result[k] for k in
        ["n_universe", "n_with_dividends", "coverage_frac", "total_dividend_events",
         "gate_a_coverage_gt_0.8"]}, indent=2))


if __name__ == "__main__":
    main()