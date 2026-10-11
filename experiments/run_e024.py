"""E024: Overnight-intraday decomposition audit.

Part A: per-strategy OOS Sharpe under three conventions (c2c, overnight-only,
intraday-only) for validated strategies.
Part B: matched-placebo z under BOTH c2c and overnight conventions.
Part C: adjusted-open data-integrity check (auto_adjust True vs False).
Part D: convention policy recorded in PRIORITIZATION.md.

Pre-registered expectations (v1.2.3): FE2 >= 40% overnight share for equity
flagship when c2c>0; FE3 intraday-only never exceeds c2c by > 0.3.
"""
import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import data, backtest, validation, strategies, macro, trend, futures

TC_COST = 0.0005
SLIPPAGE = 0.0002
TRAIN = 504
TEST = 63
STEP = 63
SEED = 42
START = "2014-01-01"
PLACEBO_N = 50

LARGE_LIQUID = [
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
]

ASSETS_3 = ["SPY", "IEF", "GLD"]

def _walkforward_metrics(close, open_, weights, spy_ret, rebalance_freq=1, tc_cost=TC_COST, slippage=SLIPPAGE, convention='overnight'):
    if convention == 'overnight':
        rets = backtest.portfolio_returns_rebalance_clean(
            weights, close, open_, tc_cost=tc_cost, slippage=slippage, rebalance_freq=rebalance_freq
        )
    elif convention == 'c2c':
        rets = backtest.portfolio_returns_close_to_close(
            weights, close, tc_cost=tc_cost, slippage=slippage, rebalance_freq=rebalance_freq
        )
    elif convention == 'intraday':
        w = backtest.shift_weights(weights)
        if rebalance_freq > 1:
            w = backtest._rebalance_weights(w, rebalance_freq)
        # weights shifted to be executed at next open; intraday return of that position is close_{t}/open_{t} if held into day?
        # Or: position set at close_{t-1} executed at open_t; held during day t, return is close_t/open_t - 1
        w = backtest.shift_weights(weights)  # executed at t+1 open
        if rebalance_freq > 1:
            w = backtest._rebalance_weights(w, rebalance_freq)

        # But weights are for positions executed at t+1 open? Wait - shift_weights shifts forward 1 day.
        # So w_s[t] corresponds to weights for execution at next open relative to when set?
        # Looking at shift_weights: returns weights.shift(1).fillna(0.0). So target set at date t becomes executable at t+1.
        # Then overnight return component is (open_{t+1}/close_t - 1) * w_s[t] where w_s is shifted weights.
        # Intraday component for the position held during day t+1 is (close_{t+1}/open_{t+1} - 1) * w_s[t].
        # So for intraday convention as specified (open-to-close), we need returns = sum_t w_s[t] * (close_{t+1}/open_{t+1} - 1) with proper alignment.
        w = backtest.shift_weights(weights)
        if rebalance_freq > 1:
            w = backtest._rebalance_weights(w, rebalance_freq)
        asset_ret = (close.shift(-1) / open_.shift(-1)) - 1.0  # open_{t+1}->close_{t+1}
        gross = (w * asset_ret).sum(axis=1)
        turnover = (w.diff().abs()).sum(axis=1)
        costs = turnover * (tc_cost + slippage)
        net = gross - costs
        rets = pd.DataFrame({"gross": gross, "costs": costs, "net": net})
    else:
        raise ValueError(convention)

    net = rets["net"].dropna()
    common = net.index.intersection(spy_ret.index)
    y = net.loc[common]
    x = spy_ret.loc[common]
    n = len(y)
    if n > 2 and x.std() > 0:
        A = np.vstack([np.ones(n), x.values]).T
        alpha, beta = np.linalg.lstsq(A, y.values, rcond=None)[0]
        corr = float(np.corrcoef(y.values, x.values)[0, 1])
    else:
        alpha, beta, corr = np.nan, np.nan, np.nan

    m = backtest.metrics(net)
    ret_dd = net
    cum = (1.0 + ret_dd).cumprod(); roll = cum.cummax(); dd_series = cum/roll-1.0; dd = float(dd_series.min()); uw = int((dd_series < 0).sum())
    pos = (net > 0).sum()
    total = len(net)
    return {
        "ret": rets,
        "net": net,
        "oos": float(m["sharpe"]),
        "oos_std": float(m.get("sharpe_std", 0.0)),
        "turnover": float(backtest.average_turnover(weights)),
        "diag": {
            "equity_beta": float(beta),
            "corr_spy": float(corr),
            "alpha_annual": float(alpha * 252),
            "is_sharpe": float(m["sharpe"]),
            "is_ann_return": float(m["annual_return"]),
            "is_ann_vol": float(m["annual_vol"]),
            "is_max_dd": float(dd),
        },
        "dd": float(dd),
        "uw": int(uw),
        "n_pos": int(pos),
        "n_total": int(total),
    }

def _overnight_share(c2c, overnight, intraday):
    # c2c ~ (1+overnight)*(1+intraday)-1; share of gross edge contribution is approximate
    # simpler: if c2c>0, share = (overnight_return_contribution) / c2c_contribution - use Sharpe? spec says "overnight share of the c2c edge"
    # report when c2c Sharpe > 0; use (overnight_sharpe / c2c_sharpe) if scaled? or just ratio of the two convention Shapres
    if c2c > 0:
        return float(overnight / c2c) if c2c != 0 else 0.0
    return 0.0

def block_permute_signal_like(signal, seed=SEED, block=21):
    """Simple block permutation for placebo - used for general signals"""
    rng = np.random.default_rng(seed)
    s = signal.copy()
    idx = s.index
    # split into blocks of ~month
    blocks = []
    for i in range(0, len(idx), block):
        blocks.append(idx[i:i+block])
    order = np.arange(len(blocks))
    rng.shuffle(order)
    perm = pd.DataFrame(index=idx, columns=s.columns)
    for j, orig in enumerate(order):
        perm.loc[blocks[orig]] = s.loc[blocks[j]].values
    return perm

def eval_equity_flagship(convention='c2c', placebo=False, seed=SEED):
    """Equity flagship: time_series_momentum_pure (12m, skip 1) with inverse-vol weights, monthly rebal."""
    df = data.download(LARGE_LIQUID, start=START)
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(close.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)

    signal = strategies.time_series_momentum_pure(close, lookback=12, skip=1)
    if placebo:
        rng = np.random.default_rng(seed)
        idx = signal.index
        blocks = [idx[i:i+21] for i in range(0, len(idx), 21)]
        order = np.arange(len(blocks)); rng.shuffle(order)
        perm = pd.DataFrame(index=idx, columns=signal.columns)
        for j, orig in enumerate(order):
            perm.loc[blocks[orig]] = signal.loc[blocks[j]].values
        signal = perm
    weights = backtest.time_series_momentum_weights(signal, close, long_only=True, vol_window=63)
    res = _walkforward_metrics(close, open_, weights, spy_ret, rebalance_freq=21, convention=convention)
    return res

def eval_reversal(convention='c2c', placebo=False, seed=SEED):
    df = data.download(LARGE_LIQUID, start=START)
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(close.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)

    signal = strategies.reversal(close, lookback=12)
    if placebo:
        rng = np.random.default_rng(seed)
        idx = signal.index
        blocks = [idx[i:i+21] for i in range(0, len(idx), 21)]
        order = np.arange(len(blocks)); rng.shuffle(order)
        perm = pd.DataFrame(index=idx, columns=signal.columns)
        for j, orig in enumerate(order):
            perm.loc[blocks[orig]] = signal.loc[blocks[j]].values
        signal = perm
    weights = backtest.equal_weight_weights(signal, long_only=True)
    res = _walkforward_metrics(close, open_, weights, spy_ret, rebalance_freq=10, convention=convention)
    return res

def eval_low_vol(convention='c2c', placebo=False, seed=SEED):
    df = data.download(LARGE_LIQUID, start=START)
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(close.index).fillna(close.index).ffill()
    spy = spy.reindex(close.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)

    signal = strategies.low_volatility(close, vol_window=63)
    if placebo:
        rng = np.random.default_rng(seed)
        idx = signal.index
        blocks = [idx[i:i+21] for i in range(0, len(idx), 21)]
        order = np.arange(len(blocks)); rng.shuffle(order)
        perm = pd.DataFrame(index=idx, columns=signal.columns)
        for j, orig in enumerate(order):
            perm.loc[blocks[orig]] = signal.loc[blocks[j]].values
        signal = perm
    weights = backtest.equal_weight_weights(signal, long_only=True)
    res = _walkforward_metrics(close, open_, weights, spy_ret, rebalance_freq=21, convention=convention)
    return res

def eval_momentum(convention='c2c', placebo=False, seed=SEED):
    df = data.download(LARGE_LIQUID, start=START)
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(close.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)
    signal = strategies.momentum(close, lookback=12)
    if placebo:
        rng = np.random.default_rng(seed)
        idx = signal.index
        blocks = [idx[i:i+21] for i in range(0, len(idx), 21)]
        order = np.arange(len(blocks)); rng.shuffle(order)
        perm = pd.DataFrame(index=idx, columns=signal.columns)
        for j, orig in enumerate(order):
            perm.loc[blocks[orig]] = signal.loc[blocks[j]].values
        signal = perm
    weights = backtest.equal_weight_weights(signal, long_only=True)
    res = _walkforward_metrics(close, open_, weights, spy_ret, rebalance_freq=1, convention=convention)
    return res

def eval_value(convention='c2c', placebo=False, seed=SEED):
    df = data.download(LARGE_LIQUID, start=START)
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(close.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)
    signal = strategies.value(close)
    if placebo:
        rng = np.random.default_rng(seed)
        idx = signal.index
        blocks = [idx[i:i+21] for i in range(0, len(idx), 21)]
        order = np.arange(len(blocks)); rng.shuffle(order)
        perm = pd.DataFrame(index=idx, columns=signal.columns)
        for j, orig in enumerate(order):
            perm.loc[blocks[orig]] = signal.loc[blocks[j]].values
        signal = perm
    weights = backtest.equal_weight_weights(signal, long_only=True)
    res = _walkforward_metrics(close, open_, weights, spy_ret, rebalance_freq=21, convention=convention)
    return res

def eval_quality(convention='c2c', placebo=False, seed=SEED):
    df = data.download(LARGE_LIQUID, start=START)
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(close.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)
    signal = strategies.quality(close)
    if placebo:
        rng = np.random.default_rng(seed)
        idx = signal.index
        blocks = [idx[i:i+21] for i in range(0, len(idx), 21)]
        order = np.arange(len(blocks)); rng.shuffle(order)
        perm = pd.DataFrame(index=idx, columns=signal.columns)
        for j, orig in enumerate(order):
            perm.loc[blocks[orig]] = signal.loc[blocks[j]].values
        signal = perm
    weights = backtest.equal_weight_weights(signal, long_only=True)
    res = _walkforward_metrics(close, open_, weights, spy_ret, rebalance_freq=21, convention=convention)
    return res

def eval_short_reversal(convention='c2c', placebo=False, seed=SEED):
    df = data.download(LARGE_LIQUID, start=START)
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(close.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)
    signal = strategies.short_reversal(close, lookback=1)
    if placebo:
        rng = np.random.default_rng(seed)
        idx = signal.index
        blocks = [idx[i:i+21] for i in range(0, len(idx), 21)]
        order = np.arange(len(blocks)); rng.shuffle(order)
        perm = pd.DataFrame(index=idx, columns=signal.columns)
        for j, orig in enumerate(order):
            perm.loc[blocks[orig]] = signal.loc[blocks[j]].values
        signal = perm
    weights = backtest.equal_weight_weights(signal, long_only=True)
    res = _walkforward_metrics(close, open_, weights, spy_ret, rebalance_freq=1, convention=convention)
    return res

def eval_mean_reversion5(convention='c2c', placebo=False, seed=SEED):
    df = data.download(LARGE_LIQUID, start=START)
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(close.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)
    signal = strategies.mean_reversion_5(close)
    if placebo:
        rng = np.random.default_rng(seed)
        idx = signal.index
        blocks = [idx[i:i+21] for i in range(0, len(idx), 21)]
        order = np.arange(len(blocks)); rng.shuffle(order)
        perm = pd.DataFrame(index=idx, columns=signal.columns)
        for j, orig in enumerate(order):
            perm.loc[blocks[orig]] = signal.loc[blocks[j]].values
        signal = perm
    weights = backtest.equal_weight_weights(signal, long_only=True)
    res = _walkforward_metrics(close, open_, weights, spy_ret, rebalance_freq=1, convention=convention)
    return res

# For futures/macro/trend, we need to be careful - they have specific implementations
# Let's add macro and trend quickly

def eval_macro(convention='c2c', placebo=False, seed=SEED):
    close, open_ = load_assets3()
    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(close.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)
    weights = macro.macro_momentum_weights(close, open_, long_only=True, rebalance_freq=21,
                                          lookback_months=6, zscore_window_months=60, release_lag_months=1,
                                          seed=seed if placebo else None, placebo=placebo)
    res = _walkforward_metrics(close, open_, weights, spy_ret, rebalance_freq=21, convention=convention)
    return res

def load_assets3():
    df = data.download(ASSETS_3, start=START)
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    return close, open_

def eval_trend(convention='c2c', placebo=False, seed=SEED):
    close, open_ = load_assets3()
    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(close.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)
    weights = trend.trend_weights(close, open_, long_only=True, rebalance_freq=21,
                                  lookbacks=(21,63,252), vol_window=63, seed=seed if placebo else None, placebo=placebo)
    res = _walkforward_metrics(close, open_, weights, spy_ret, rebalance_freq=21, convention=convention)
    return res

def eval_strategy(name, convention='c2c', placebo=False, seed=SEED):
    if name == 'time_series_momentum':
        return eval_equity_flagship(convention, placebo, seed)
    elif name == 'reversal':
        return eval_reversal(convention, placebo, seed)
    elif name == 'low_vol':
        return eval_low_vol(convention, placebo, seed)
    elif name == 'momentum':
        return eval_momentum(convention, placebo, seed)
    elif name == 'value':
        return eval_value(convention, placebo, seed)
    elif name == 'quality':
        return eval_quality(convention, placebo, seed)
    elif name == 'short_reversal':
        return eval_short_reversal(convention, placebo, seed)
    elif name == 'mean_reversion_5':
        return eval_mean_reversion5(convention, placebo, seed)
    elif name == 'macro':
        return eval_macro(convention, placebo, seed)
    elif name == 'trend':
        return eval_trend(convention, placebo, seed)
    else:
        raise ValueError(name)
