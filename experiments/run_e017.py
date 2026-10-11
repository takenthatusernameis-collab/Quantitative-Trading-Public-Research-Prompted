#!/usr/bin/env python3
"""E017: TSM + carry on an extended (2014-2026) properly-rolled futures panel.

Follows up the E016 handoff. E016's panel was truncated to 2017-07-10 because
RTY=F data on yfinance starts then, leaving only 28 OOS folds in a difficult
trend-following regime. E017 restores the full 2014-2026 sample by dropping
RTY=F and adding breadth (HG/ZW/ZS/KC + spot-ETF pairs CPER/WEAT/SOYB/CORN).

Design:
  - Universe: 17 liquid futures contracts across equities, bonds,
    commodities and FX, each paired with a spot ETF for seam detection
    and carry construction.
  - Walk-forward 504/63/63 (~42 OOS folds), monthly (21d) rebalance,
    next-day-open execution (close-to-close for the de-seamed index,
    whose open prices are not observable), tc=0.5bps + slippage=0.2bps.
  - TSM: PRE-REGISTERED 9-month lookback (justified from the E016 short-
    sample grid: 9m and 18m both hit 0.89 vs 12m at 0.72; 9m chosen as
    the shortest robust horizon, minimizing lookback degrees of freedom).
    1-month skip, inverse-vol (63d), symmetric long/short.
  - Carry: dollar-neutral top/bottom-half sort, inverse-vol weighted.
  - Pre-registered promotion gates: OOS Sharpe >= 1.0, placebo z >= 3,
    positive bear Sharpe, |beta| <= 0.2.
"""

import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import data, backtest, strategies, futures

TC_COST = 0.0005
SLIPPAGE = 0.0002
TRAIN = 504
TEST = 63
STEP = 63
REBAL = 21
SEED = 42
PLACEBO_N_SIM = 50

START = "2014-01-01"

# Futures ticker -> (paired spot ETF, roll cadence).
# E016 universe minus RTY=F (data starts 2017-07) plus breadth.
FUTURES_UNIVERSE = {
    "ES=F": ("SPY", "quarterly"),
    "NQ=F": ("QQQ", "quarterly"),
    "YM=F": ("DIA", "quarterly"),
    "ZB=F": ("TLT", "quarterly"),
    "ZN=F": ("IEF", "quarterly"),
    "GC=F": ("GLD", "monthly"),
    "SI=F": ("SLV", "monthly"),
    "CL=F": ("USO", "monthly"),
    "NG=F": ("UNG", "monthly"),
    "HG=F": ("CPER", "monthly"),
    "ZW=F": ("WEAT", "monthly"),
    "ZS=F": ("SOYB", "monthly"),
    "ZC=F": ("CORN", "monthly"),
    "6E=F": ("FXE", "quarterly"),
    "6B=F": ("FXF", "quarterly"),
    "6J=F": ("FXY", "quarterly"),
}

# Pre-registered primary lookback (months). See module docstring for
# justification; 6/9/12/18m reported as sensitivity with multiple-testing
# awareness, NOT used to select the primary.
PRIMARY_LOOKBACK = 9
