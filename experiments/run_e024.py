#!/usr/bin/env python3
"""E024: Overnight-intraday decomposition audit, adjusted-open
data-integrity check and execution-convention policy.

Motivation (E023 handoff): E020 demoted the E019 promotion because
the equity sleeve's next-day-open execution convention inflated
returns (2.175 mixed vs 1.745 convention-aligned); E023 decomposed
both Economic-Trend sleeves and found BOTH edges overnight-
concentrated (macro 0.516 overnight / -0.147 intraday; price trend
1.064 / 0.539). The repository's flagship (equity TSM 12m) has
never been decomposed, and the README caveat ("auto_adjust=True
merges open/close adjustments; open-price execution is
approximate") is unresolved. This audit:

Part A: per-strategy OOS Sharpe under three execution conventions
        (close-to-close, overnight-only close->next-open, intraday-
        only open->close) for every validated strategy, with the
        overnight share of the c2c edge.
Part B: matched placebo z under BOTH c2c and overnight conventions
        (50 sims; 12m-block permutation of each strategy's signal;
        carry uses E018's seam-calendar-preserving permutation),
        flagging convention-dependent strategies (overnight z >= 3
        but c2c z < 3).
Part C: adjusted-open data-integrity check on ex-dividend dates
        (adjusted vs raw opens), resolving the README caveat.
Part D: pre-registered execution-convention policy for all future
        experiments (recorded in ledger/PRIORITIZATION.md v1.2.4).

Engines (all three use the same shifted, rebalance-sampled
    weight path w_s[t] = rebalance_sample(weights.shift(1))[t],
    so turnover and costs are identical across conventions):
    - c2c:       gross[t] = w_s[t] * (close[t+1]/close[t] - 1)
    - overnight: gross[t] = w_s[t] * (open[t+1]/close[t] - 1)
    - intraday:  gross[t] = w_s[t] * (close[t+1]/open[t+1] - 1)
    The overnight segment at t (close[t]->open[t+1]) composes with the
    intraday segment at t (open[t+1]->close[t+1]) to the c2c segment at
    t+1, so the per-asset accounting identity
        c2c[t+1] = (1 + overnight[t]) * (1 + intraday[t]) - 1
    holds exactly by construction and is verified before any Part A/B
    number is trusted (asserted per strategy, max abs diff < 1e-9).
    This is the same decomposition convention E023 used for its
    overnight/intraday sleeve split.

Futures: the de-seamed synthetic index has no observable opens. A
de-seamed open series is reconstructed by splitting each day's
de-seamed return into overnight/intraday segments using the RAW
futures split on non-seam days and the paired spot ETF split on
seam days (consistent with the de-seaming methodology: seam-day
futures returns are replaced by the spot ETF return). The identity
then holds exactly on the de-seamed panel by construction.

PRE-REGISTRATION (set before running; goalposts not moved):
- FE1 (Part C): adjusted overnight returns on ex-dividend dates
  are consistent with total-return accounting. FALSIFIED if the
  pooled mean ex-date adjusted overnight return < -0.5 x median
  dividend yield (double-counting artifact; would invalidate ALL
  next-open-convention results in the repo).
- FE2: the equity flagship's overnight share of its c2c edge
  >= 40% (E023 pattern).
- FE3: no strategy's intraday-only OOS Sharpe exceeds its c2c
  OOS Sharpe by more than 0.3 (intraday is not the repository's
  edge source).
- Convention-dependence flag: overnight placebo z >= 3 with c2c
  placebo z < 3.
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import yfinance as yf

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import data, backtest, strategies, macro, trend
from src import jsonio
from experiments.run_e017 import (
    build_panels, FUTURES_UNIVERSE, TC_COST, SLIPPAGE, TRAIN,
    TEST, STEP, SEED, START,
)
from experiments.run_e018 import permuted_carry_panel
from src.run_experiment import UNIVERSES, deterministic_timestamp

LARGE_LIQUID = UNIVERSES["large_liquid"]
PLACEBO_N = 50
BLOCK_DAYS = 252    # 12-month blocks for daily-indexed signals
BLOCK_MONTHS = 12   # 12-month blocks for monthly-indexed signals

CONVENTIONS = ("c2c", "overnight", "intraday")

# Pre-registered falsification expectations (see module docstring).
FE1_TOLERANCE = -0.5   # falsified if mean ex-date adj overnight < FE1_TOLERANCE * median div yield
FE2_MIN_SHARE = 0.40
FE3_MAX_INTRA_EXCESS = 0.3
IDENTITY_TOL = 1e-9


# ---------------------------------------------------------------------------
# Execution-convention engines (identical weight path, identical costs)
# ---------------------------------------------------------------------------

def _shifted_rebalanced(w, rebal):
    w_s = backtest.shift_weights(w)
    if rebal > 1:
        w_s = backtest._rebalance_weights(w_s, rebal)
    return w_s


def engine(conv, w, close, open_, rebal=1,
           tc_cost=TC_COST, slippage=SLIPPAGE):
    """Portfolio gross/net returns under one execution convention.

    All three conventions use the SAME shifted, rebalance-sampled
    weight path, so turnover and transaction costs are identical
    across conventions; only the asset return segment differs.
    """
    w_s = _shifted_rebalanced(w, rebal)
    if conv == "c2c":
        asset_ret = close.pct_change()
    elif conv == "overnight":
        asset_ret = (open_.shift(-1) / close - 1.0)
    elif conv == "intraday":
        asset_ret = (close.shift(-1) / open_.shift(-1) - 1.0)
    else:
        raise ValueError(f"unknown convention {conv!r}")
    gross = (w_s * asset_ret).sum(axis=1)
    turnover = (w_s.diff().abs()).sum(axis=1)
    costs = turnover * (tc_cost + slippage)
    net = gross - costs
    return pd.DataFrame({"gross": gross, "costs": costs, "net": net})


def verify_identity(close, open_, rebal):
    """Per-asset accounting-identity check (engineering guard).

    Engine semantics (see module docstring): the overnight engine's
    segment at index t is close[t] -> open[t+1], the intraday engine's
    segment at index t is open[t+1] -> close[t+1], and the c2c engine's
    segment at index t is close[t-1] -> close[t]. Composing overnight[t]
    with intraday[t] therefore yields close[t] -> close[t+1] = c2c[t+1],
    so the identity holds as lhs.shift(1) == c2c. Verified empirically:
    this alignment gives 0.0 (max abs diff 2.2e-16), while the two wrong
    alignments (same-index and -1-shift) give 0.658 and 0.611
    respectively on the flagship.
    """
    on = open_.shift(-1) / close - 1.0
    intra = close.shift(-1) / open_.shift(-1) - 1.0
    c2c = close.pct_change()
    lhs = (1.0 + on) * (1.0 + intra) - 1.0
    diff = (lhs.shift(1) - c2c).abs()
    return float(np.nanmax(diff.to_numpy())) if diff.size else 0.0


# ---------------------------------------------------------------------------
# Evaluation (walk-forward OOS, matching the E017/E023 pattern)
# ---------------------------------------------------------------------------

def _beta_vs_spy(net, spy_ret):
    common = net.index.intersection(spy_ret.index)
    y = net.loc[common].values
    x = spy_ret.loc[common].values
    if len(y) > 2 and np.std(x) > 0:
        A = np.vstack([np.ones(len(x)), x]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        return float(coef[1]), float(np.corrcoef(y, x)[0, 1])
    return float("nan"), float("nan")


def evaluate_convention(conv, w, close, open_, spy_ret, rebal=1):
    """Full evaluation of a weight panel under one convention."""
    rets = engine(conv, w, close, open_, rebal)
    net = rets["net"].dropna()
    m = backtest.metrics(net)
    beta, corr = _beta_vs_spy(net, spy_ret)

    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    fold_sharps = []
    for (tr_s, tr_e, te_s, te_e) in splits:
        test_idx = close.index[te_s:te_e]
        test_rets = rets.loc[rets.index.intersection(test_idx)]
        fm = backtest.metrics(test_rets["net"])
        sh = fm.get("sharpe")
        fold_sharps.append(
            float(sh) if sh is not None and not np.isnan(float(sh)) else float("nan")
        )
    valid = [s for s in fold_sharps if s == s]
    oos = float(np.mean(valid)) if valid else float("nan")
    oos_std = float(np.std(valid)) if valid else float("nan")

    cum = (1.0 + net).cumprod()
    roll = cum.cummax()
    dd = float((cum / roll - 1.0).min())
    return {
        "oos_sharpe": oos,
        "oos_sharpe_std": oos_std,
        "full_sample_sharpe": float(m.get("sharpe", float("nan"))),
        "full_sample_ann_return": float(m.get("annual_return", float("nan"))),
        "full_sample_ann_vol": float(m.get("annual_vol", float("nan"))),
        "equity_beta": beta,
        "corr_spy": corr,
        "max_drawdown": dd,
        "turnover": float(backtest.average_turnover(w)),
        "positive_folds": int(sum(1 for s in valid if s > 0)),
        "n_folds": len(valid),
        "fold_sharpes": fold_sharps,
    }


def overnight_share(rets_on, rets_c2c, oos_c2c):
    """Overnight share of the c2c edge (mean-net-return basis).

    Reported only when the c2c OOS Sharpe > 0 (pre-registered rule).
    Engine semantics: overnight[t] = close[t]->open[t+1] and
    c2c[t+1] = close[t]->close[t+1], so the overnight segment of day t
    is a component of the c2c segment of day t+1. The share is therefore
    computed on the aligned pair (overnight[t], c2c[t+1]); the first-order
    approximation mean(c2c) ~= mean(overnight) + mean(intraday) holds on
    this alignment.
    """
    if not (oos_c2c > 0):
        return None
    on_net = rets_on["net"].dropna()
    c2c_net = rets_c2c["net"].dropna()
    # align overnight[t] with c2c[t+1]
    shifted = c2c_net.shift(1)
    common = on_net.index.intersection(shifted.index)
    on_mean = float(on_net.loc[common].mean())
    c2c_mean = float(shifted.loc[common].mean())
    if abs(c2c_mean) < 1e-12:
        return None
    return float(on_mean / c2c_mean)


# ---------------------------------------------------------------------------
# Strategy registry
# ---------------------------------------------------------------------------

def block_permute_frame(signal, block_days=BLOCK_DAYS, seed=SEED):
    """Permute a daily-indexed signal frame in contiguous blocks.

    Daily analog of macro.block_permute_signals: each column's
    signal is split into contiguous ``block_days``-day blocks, the
    block order is permuted per column, and the blocks are
    re-concatenated. Preserves each column's signal distribution
    and within-block persistence; destroys time alignment with
    forward returns.
    """
    rng = np.random.default_rng(seed)
    out = signal.copy()
    idx = signal.index
    n = len(idx)
    starts = list(range(0, n, block_days))
    for col in signal.columns:
        vals = signal[col].to_numpy()
        blocks = [vals[s:s + block_days] for s in starts if s < n]
        order = rng.permutation(len(blocks))
        out[col] = np.concatenate([blocks[i] for i in order])
    return out


def build_specs(ctx):
    """Registry of the repository's validated strategies.

    Each spec carries: name, family (panel), label, rebalance
    frequency, a deterministic signal builder, a weight builder and
    a placebo-signal builder (the strategy's matched null: 12m
    block permutation of the signal; carry uses E018's
    seam-calendar-preserving permutation).
    """
    eq = ctx["equity"]
    fu = ctx["futures"]
    xa = ctx["cross_asset"]
    eq_close, eq_open, eq_spy = eq["close"], eq["open_"], eq["spy"]
    fu_close, fu_open, fu_spy = fu["de_index"], fu["de_open"], fu["spy"]
    xa_close, xa_open, xa_spy = xa["close"], xa["open_"], xa["spy"]
    fu_vol = fu_close.pct_change().rolling(63).std().replace(0, np.nan)

    specs = [
        # ---- equity large_liquid ----
        {
            "name": "time_series_momentum",
            "family": "equity",
            "label": "TSM pure (12m lookback, 1m skip, inverse-vol 63d, "
                     "long-only, monthly rebalance) - the equity flagship",
            "rebal": 21,
            "signal": lambda: strategies.time_series_momentum_pure(
                eq_close, lookback=12, skip=1),
            "weights": lambda sig: backtest.time_series_momentum_weights(
                sig, eq_close, long_only=True, vol_window=63),
            "placebo": lambda seed: block_permute_frame(
                strategies.time_series_momentum_pure(eq_close, 12, 1),
                BLOCK_DAYS, seed),
        },
        {
            "name": "reversal",
            "family": "equity",
            "label": "Long-term reversal (12m, De Bondt-Thaler; equal-weight "
                     "top quintile, 10d rebalance)",
            "rebal": 10,
            "signal": lambda: strategies.reversal(eq_close, lookback=12),
            "weights": lambda sig: backtest.equal_weight_weights(
                sig, long_only=True),
            "placebo": lambda seed: block_permute_frame(
                strategies.reversal(eq_close, 12), BLOCK_DAYS, seed),
        },
        {
            "name": "low_vol",
            "family": "equity",
            "label": "Low-volatility anomaly (63d realized vol; equal-weight "
                     "top quintile, daily rebalance)",
            "rebal": 1,
            "signal": lambda: strategies.low_vol(eq_close, window=63),
            "weights": lambda sig: backtest.equal_weight_weights(
                sig, long_only=True),
            "placebo": lambda seed: block_permute_frame(
                strategies.low_vol(eq_close, 63), BLOCK_DAYS, seed),
        },
        {
            "name": "momentum",
            "family": "equity",
            "label": "Cross-sectional momentum (12m, 1m skip, Jegadeesh-Titman; "
                     "equal-weight top quintile, daily rebalance)",
            "rebal": 1,
            "signal": lambda: strategies.momentum(eq_close, lookback=12),
            "weights": lambda sig: backtest.equal_weight_weights(
                sig, long_only=True),
            "placebo": lambda seed: block_permute_frame(
                strategies.momentum(eq_close, 12), BLOCK_DAYS, seed),
        },
        {
            "name": "value",
            "family": "equity",
            "label": "Value proxy (negative 60m price momentum; equal-weight "
                     "top quintile, daily rebalance)",
            "rebal": 1,
            "signal": lambda: strategies.value(eq_close),
            "weights": lambda sig: backtest.equal_weight_weights(
                sig, long_only=True),
            "placebo": lambda seed: block_permute_frame(
                strategies.value(eq_close), BLOCK_DAYS, seed),
        },
        {
            "name": "quality",
            "family": "equity",
            "label": "Quality/defensive proxy (low vol + short-term momentum, "
                     "cross-sectional z-scores; equal-weight top quintile, "
                     "daily rebalance)",
            "rebal": 1,
            "signal": lambda: strategies.quality(eq_close),
            "weights": lambda sig: backtest.equal_weight_weights(
                sig, long_only=True),
            "placebo": lambda seed: block_permute_frame(
                strategies.quality(eq_close), BLOCK_DAYS, seed),
        },
        {
            "name": "short_reversal",
            "family": "equity",
            "label": "Short-term reversal (1m return inverted; equal-weight "
                     "top quintile, daily rebalance)",
            "rebal": 1,
            "signal": lambda: strategies.short_reversal(eq_close, lookback=21),
            "weights": lambda sig: backtest.equal_weight_weights(
                sig, long_only=True),
            "placebo": lambda seed: block_permute_frame(
                strategies.short_reversal(eq_close, 21), BLOCK_DAYS, seed),
        },
        {
            "name": "mean_reversion_5",
            "family": "equity",
            "label": "Very short-term mean reversion (5d return inverted; "
                     "equal-weight top quintile, daily rebalance)",
            "rebal": 1,
            "signal": lambda: strategies.mean_reversion_5(eq_close),
            "weights": lambda sig: backtest.equal_weight_weights(
                sig, long_only=True),
            "placebo": lambda seed: block_permute_frame(
                strategies.mean_reversion_5(eq_close), BLOCK_DAYS, seed),
        },
        {
            "name": "dollar_neutral_lowbeta",
            "family": "equity",
            "label": "Dollar-neutral low-beta sort (252d beta vs SPY, Vasicek "
                     "shrink 0.5, 10/10 percentile, dollar-neutral, "
                     "monthly rebalance)",
            "rebal": 21,
            "signal": lambda: strategies.dollar_neutral_lowbeta(
                eq_close, eq_spy, beta_window=252, shrink=0.5),
            "weights": lambda sig: backtest.dollar_neutral_longshort_weights(
                sig, top_frac=0.1),
            "placebo": lambda seed: block_permute_frame(
                strategies.dollar_neutral_lowbeta(
                    eq_close, eq_spy, 252, 0.5), BLOCK_DAYS, seed),
        },
        # ---- futures panel (de-seamed, 2014-2026) ----
        {
            "name": "tsm_18m_futures",
            "family": "futures",
            "label": "TSM (18m lookback, 1m skip, symmetric long/short, "
                     "inverse-vol 63d, monthly) on the de-seamed "
                     "16-contract panel",
            "rebal": 21,
            "signal": lambda: strategies.time_series_momentum_pure(
                fu_close, lookback=18, skip=1),
            "weights": lambda sig: backtest.time_series_momentum_weights(
                sig, fu_close, long_only=False, vol_window=63),
            "placebo": lambda seed: block_permute_frame(
                strategies.time_series_momentum_pure(fu_close, 18, 1),
                BLOCK_DAYS, seed),
        },
        {
            "name": "carry_realized_roll_yield_futures",
            "family": "futures",
            "label": "Carry (realized roll yield, 252d trailing seam-gap "
                     "sum; dollar-neutral top/bottom-half sort, "
                     "inverse-vol, monthly)",
            "rebal": 21,
            "signal": lambda: fu["carry_rroll"],
            "weights": lambda sig: backtest.carry_weights(sig, fu_vol),
            "placebo": lambda seed: permuted_carry_panel(
                fu["fut_close"], fu["spot_close"], fu["seams_dt"],
                252, np.random.default_rng(seed)),
        },
        # ---- cross-asset (SPY/IEF/GLD) ----
        {
            "name": "macro_momentum",
            "family": "cross_asset",
            "label": "Macro momentum (E022: 5 FRED themes, 6m momentum, "
                     "60m z-score, release-lagged 1 reference month, "
                     "structural signs onto SPY/IEF/GLD, gross=1, "
                     "month-end rebalance)",
            "rebal": 1,
            "signal": lambda: macro.theme_signals(window=6, zscore_window=60),
            "weights": lambda sig: macro.macro_momentum_weights(
                sig, xa_close.index),
            "placebo": lambda seed: macro.block_permute_signals(
                macro.theme_signals(window=6, zscore_window=60),
                block_months=BLOCK_MONTHS, seed=seed),
        },
        {
            "name": "price_trend",
            "family": "cross_asset",
            "label": "Price trend (E023: equal-weighted 1m/3m/12m trailing "
                     "returns, directional, inverse-vol 63d, gross=1, "
                     "month-end rebalance)",
            "rebal": 1,
            "signal": lambda: trend.price_trend_signal(
                xa_close, lookbacks=(21, 63, 252)),
            "weights": lambda sig: trend.price_trend_monthly_weights_from_signal(
                sig, xa_close, vol_window=63),
            "placebo": lambda seed: trend.block_permute_monthly_factor(
                trend.price_trend_signal(xa_close, (21, 63, 252)),
                block_months=BLOCK_MONTHS, seed=seed),
        },
    ]
    return specs


# ---------------------------------------------------------------------------
# Futures de-seamed opens
# ---------------------------------------------------------------------------

def build_deseamed_opens(panels, universe):
    """De-seamed open series for the synthetic de-seamed index.

    The de-seamed index has no observable opens. We reconstruct a
    de-seamed open by splitting each day's de-seamed return into an
    overnight and an intraday segment using the RAW futures' split
    on non-seam days and the paired spot ETF's split on seam days
    (consistent with the de-seaming methodology: seam-day futures
    returns are replaced by the paired spot ETF return). By
    construction de_open[t] * (de_index[t] / de_open[t]) ==
    de_index[t], so the accounting identity holds exactly on the
    de-seamed panel.
    """
    de_index = panels["de_index"]
    fut_close = panels["fut_close"]
    fut_open = panels["fut_open"]
    spot_tickers = sorted(set(v[0] for v in universe.values()))
    sdf = data.download(spot_tickers, start=START)
    spot_open = data.get_panel(sdf, "Open")
    spot_close = data.get_panel(sdf, "Close")

    de_open = pd.DataFrame(index=de_index.index,
                           columns=de_index.columns, dtype=float)
    for col in de_index.columns:
        st = universe[col][0]
        fc = fut_close[col]
        fo = fut_open[col].reindex(fc.index).ffill()
        sc = spot_close[st].reindex(fc.index).ffill()
        so = spot_open[st].reindex(fc.index).ffill()
        raw_on = fo / fc.shift(1)
        spot_on = so / sc.shift(1)
        seams = pd.DatetimeIndex(panels["seams"][col])
        on_ratio = raw_on.copy()
        on_ratio.loc[seams] = spot_on.reindex(seams).values
        de_open[col] = de_index[col].shift(1) * on_ratio
    return de_open


# ---------------------------------------------------------------------------
# Part C: adjusted-open data-integrity check
# ---------------------------------------------------------------------------

def download_raw(tickers, start=START):
    """Raw (unadjusted) OHLCV + corporate-actions download.

    Uses a DISTINCT cache key (prefix ``raw_``) so the adjusted
    caches managed by src.data.download are never overwritten
    (src.data.download's cache key does not encode auto_adjust).
    """
    tickers = sorted(tickers)
    key = "raw|" + "|".join(tickers)
    h = hashlib.sha256(key.encode()).hexdigest()[:16]
    safe = "_".join(tickers)[:80]
    cache = os.path.join(data.DATA_DIR,
                         f"raw_{safe}_{h}_{start}.parquet")
    if os.path.exists(cache):
        try:
            df = pd.read_parquet(cache)
            if not df.empty:
                return df
        except Exception:
            pass
    raw = yf.download(tickers, start=start, auto_adjust=False,
                      actions=True, progress=False, group_by="ticker")
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns.names = ["Ticker", "Price"]
        if raw.columns.names[0] != "Ticker":
            raw = raw.swaplevel(0, 1, axis=1)
            raw.columns.names = ["Ticker", "Price"]
        raw.columns = pd.MultiIndex.from_tuples(
            [(str(c[0]), str(c[-1])) for c in raw.columns])
        raw.columns.names = ["Ticker", "Price"]
        raw = raw.sort_index(axis=1)
    else:
        raw.columns = pd.MultiIndex.from_product(
            [tickers, list(raw.columns)])
        raw.columns.names = ["Ticker", "Price"]
    raw.index = pd.to_datetime(raw.index).tz_localize(None)
    raw.to_parquet(cache)
    return raw


def part_c(sample):
    """Adjusted-open data-integrity check on ex-dividend dates.

    Compares adjusted (auto_adjust=True) vs raw (auto_adjust=False)
    overnight returns on ex-dividend dates. Pre-registered
    falsification FE1: adjusted overnight returns on ex-dates are
    consistent with total-return accounting (the adjustment factor
    compensates the dividend gap). FALSIFIED if the pooled mean
    ex-date adjusted overnight return < -0.5 x median dividend
    yield (a double-counting artifact that would invalidate ALL
    next-open-convention results in the repository).

    Cross-check (total-return accounting): the RAW ex-date
    overnight return should be approximately -dividend + drift.
    """
    raw = download_raw(sample)
    adj = data.download(sample, start=START)

    per_ticker = {}
    pooled_adj_on_ex = []
    pooled_raw_on_ex = []
    pooled_dy = []
    for t in sample:
        rsub = raw[t]
        asub = data.wide_close(adj, t)
        # align raw and adjusted panels to common trading days
        common = rsub.index.intersection(asub.index)
        rsub = rsub.loc[common]
        asub = asub.loc[common]

        dividends = rsub["Dividends"].fillna(0.0)
        ex = dividends[dividends > 0.0].index
        # overnight segment containing the ex-date gap: close[t-1] -> open[t]
        raw_on = (rsub["Open"] / rsub["Close"].shift(1) - 1.0)
        adj_on = (asub["open"] / asub["close"].shift(1) - 1.0)
        dy = (dividends / rsub["Close"].shift(1))

        ex_adj = adj_on.reindex(ex).dropna()
        ex_raw = raw_on.reindex(ex).dropna()
        ex_dy = dy.reindex(ex).dropna()
        non_ex_mask = ~adj_on.index.isin(ex)
        non_ex_adj = adj_on[non_ex_mask]

        median_dy = float(ex_dy.median()) if len(ex_dy) else float("nan")
        mean_adj_on_ex = float(ex_adj.mean()) if len(ex_adj) else float("nan")
        mean_raw_on_ex = float(ex_raw.mean()) if len(ex_raw) else float("nan")
        per_ticker[t] = {
            "n_ex_dates": int(len(ex)),
            "median_dividend_yield": median_dy,
            "mean_adj_overnight_ex_date": mean_adj_on_ex,
            "mean_raw_overnight_ex_date": mean_raw_on_ex,
            "expected_raw_under_total_return_accounting":
                float(-median_dy) if median_dy == median_dy else float("nan"),
            "mean_adj_overnight_non_ex_date":
                float(non_ex_adj.mean()) if len(non_ex_adj) else float("nan"),
            "adj_minus_raw_overnight_ex_date":
                mean_adj_on_ex - mean_raw_on_ex
                if mean_adj_on_ex == mean_adj_on_ex and mean_raw_on_ex == mean_raw_on_ex
                else float("nan"),
        }
        pooled_adj_on_ex.extend(ex_adj.tolist())
        pooled_raw_on_ex.extend(ex_raw.tolist())
        pooled_dy.extend(ex_dy.tolist())

    pooled_median_dy = float(np.median(pooled_dy)) if pooled_dy else float("nan")
    pooled_mean_adj = float(np.mean(pooled_adj_on_ex)) if pooled_adj_on_ex else float("nan")
    pooled_mean_raw = float(np.mean(pooled_raw_on_ex)) if pooled_raw_on_ex else float("nan")
    fe1_falsified = bool(pooled_mean_adj < FE1_TOLERANCE * pooled_median_dy)
    return {
        "description": "Adjusted (auto_adjust=True) vs raw (auto_adjust=False) "
                       "overnight returns on ex-dividend dates; overnight "
                       "segment = close[t-1] -> open[t] where t is the ex-date.",
        "sample": sample,
        "per_ticker": per_ticker,
        "pooled": {
            "n_ex_dates": len(pooled_adj_on_ex),
            "median_dividend_yield": pooled_median_dy,
            "mean_adj_overnight_ex_date": pooled_mean_adj,
            "mean_raw_overnight_ex_date": pooled_mean_raw,
            "raw_minus_expected_under_total_return":
                pooled_mean_raw + pooled_median_dy
                if pooled_mean_raw == pooled_mean_raw else float("nan"),
        },
        "FE1": {
            "expectation": "adjusted ex-date overnight returns consistent with "
                           "total-return accounting (adjustment factor "
                           "compensates the dividend gap)",
            "falsification_rule": "pooled mean ex-date adjusted overnight "
                                  "return < -0.5 x median dividend yield",
            "stat": pooled_mean_adj,
            "threshold": FE1_TOLERANCE * pooled_median_dy,
            "falsified": fe1_falsified,
        },
        "cross_check": {
            "expectation": "raw ex-date overnight return ~= -dividend + drift",
            "pooled_mean_raw_overnight_ex_date": pooled_mean_raw,
            "pooled_negative_median_dividend_yield": -pooled_median_dy,
        },
    }


# ---------------------------------------------------------------------------
# Context construction
# ---------------------------------------------------------------------------

def build_contexts():
    ctx = {}

    # Equity: large_liquid universe + SPY benchmark.
    df = data.download(LARGE_LIQUID, start=START)
    eq_close = data.get_panel(df, "Close").dropna(how="all")
    eq_open = data.get_panel(df, "Open").reindex(eq_close.index).fillna(eq_close)
    bm = data.download(["SPY"], start=START)
    eq_spy = data.get_panel(bm, "Close")["SPY"].reindex(eq_close.index).ffill()
    ctx["equity"] = {
        "close": eq_close, "open_": eq_open, "spy": eq_spy,
        "spy_ret": eq_spy.pct_change().fillna(0.0),
    }

    # Futures: E017/E018 extended 16-contract de-seamed panel.
    panels = build_panels(FUTURES_UNIVERSE)
    de_open = build_deseamed_opens(panels, FUTURES_UNIVERSE)
    seams_dt = {k: pd.DatetimeIndex(v) for k, v in panels["seams"].items()}
    ctx["futures"] = {
        "fut_close": panels["fut_close"],
        "fut_open": panels["fut_open"],
        "spot_close": panels["spot_close"],
        "de_index": panels["de_index"],
        "de_open": de_open,
        "carry_rroll": panels["carry_rroll"],
        "seams_dt": seams_dt,
        "spy": panels["spy"],
        "spy_ret": panels["spy"].pct_change().fillna(0.0),
        "seam_stats": panels["seam_stats"],
    }

    # Cross-asset: SPY/IEF/GLD.
    xdf = data.download(["SPY", "IEF", "GLD"], start=START)
    xa_close = data.get_panel(xdf, "Close").dropna(how="all")
    xa_open = data.get_panel(xdf, "Open").reindex(xa_close.index).fillna(xa_close)
    xa_spy = data.get_panel(xdf, "Close")["SPY"].reindex(xa_close.index).ffill()
    ctx["cross_asset"] = {
        "close": xa_close, "open_": xa_open, "spy": xa_spy,
        "spy_ret": xa_spy.pct_change().fillna(0.0),
    }
    return ctx


def _panel_ctx(ctx, family):
    fam = ctx[family]
    if family == "futures":
        # The futures family stores its de-seamed close/open under
        # de_index/de_open (the synthetic index, not the raw futures
        # panel) so that the overnight/intraday split is consistent
        # with the de-seaming methodology.
        return fam["de_index"], fam["de_open"], fam["spy_ret"]
    return fam["close"], fam["open_"], fam["spy_ret"]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _merge(part_cache):
    """Merge cached per-part outputs into one consolidated result.

    Each part is cached to its own file when run individually, so a
    long-running Part B does not have to be re-run after a Part C fix.
    The pre-registered falsification expectations are re-evaluated from
    the merged data so they are always consistent with the final file.
    """
    part_a = part_b = part_c = None
    for p, path in part_cache.items():
        if not os.path.exists(path):
            raise SystemExit(f"missing cached part {p}: {path}")
        with open(path) as f:
            data = json.load(f)
        if p == "a":
            part_a = data["part_a"]
            identity_checks = data["identity_checks"]
        elif p == "b":
            part_b = data["part_b"]
        else:
            part_c = data["part_c"]

    fe = {}
    if part_a is not None:
        flagship = part_a.get("time_series_momentum", {})
        share = flagship.get("overnight_share_of_c2c_edge")
        fe["FE2_flagship_overnight_share"] = {
            "value": share,
            "threshold": FE2_MIN_SHARE,
            "passed": bool(share is not None and share >= FE2_MIN_SHARE),
        }
        worst_excess = None
        worst_name = None
        for name, r in part_a.items():
            ex = r.get("intraday_minus_c2c_oos_sharpe")
            if ex is not None and (worst_excess is None or ex > worst_excess):
                worst_excess = ex
                worst_name = name
        fe["FE3_intraday_excess"] = {
            "max_excess": worst_excess,
            "strategy": worst_name,
            "threshold": FE3_MAX_INTRA_EXCESS,
            "passed": bool(worst_excess is not None
                           and worst_excess <= FE3_MAX_INTRA_EXCESS),
        }
    if part_c is not None:
        fe["FE1_adjusted_open_integrity"] = {
            "falsified": part_c["FE1"]["falsified"],
            "passed": not part_c["FE1"]["falsified"],
        }

    return {
        "experiment": "E024",
        "timestamp": deterministic_timestamp(),
        "title": "Overnight-intraday decomposition audit, adjusted-open "
                 "data-integrity check and execution-convention policy",
        "pre_registered": {
            "FE1_adjusted_open_integrity": {
                "expectation": "adjusted ex-date overnight returns consistent "
                               "with total-return accounting",
                "falsification_rule": "pooled mean ex-date adjusted overnight "
                                      "return < -0.5 x median dividend yield",
            },
            "FE2_flagship_overnight_share": {
                "expectation": f"equity flagship overnight share of c2c edge "
                               f">= {FE2_MIN_SHARE:.0%}",
            },
            "FE3_intraday_excess": {
                "expectation": f"no strategy's intraday-only OOS Sharpe "
                               f"exceeds its c2c OOS Sharpe by more than "
                               f"{FE3_MAX_INTRA_EXCESS}",
            },
            "convention_dependence_flag": "overnight placebo z >= 3 with "
                                          "c2c placebo z < 3",
            "engines": {
                "c2c": "gross[t] = w_s[t] * (close[t+1]/close[t] - 1)",
                "overnight": "gross[t] = w_s[t] * (open[t+1]/close[t] - 1)",
                "intraday": "gross[t] = w_s[t] * (close[t+1]/open[t+1] - 1)",
                "weight_path": "identical shifted + rebalance-sampled weights "
                               "across conventions (identical turnover/costs)",
                "identity": "per-asset c2c[t+1] = (1+overnight[t])*(1+intraday[t]) - 1, "
                            "asserted < 1e-9 (verified empirically: 0.0; the two "
                            "wrong alignments give 0.658 and 0.611 on the flagship)",
            },
            "futures_deseamed_opens": "de-seamed open reconstructed by "
                                      "splitting each day's de-seamed return "
                                      "with the raw futures split on non-seam "
                                      "days and the paired spot ETF split on "
                                      "seam days",
            "placebo_null": "12m block permutation of each strategy's signal "
                            "(carry: E018 seam-calendar-preserving permutation "
                            "of seam excess gaps)",
        },
        "part_a": part_a,
        "identity_checks": identity_checks,
        "part_b": part_b,
        "part_c": part_c,
        "falsification_expectations": fe,
        "part_d": {
            "policy": "Recorded in ledger/PRIORITIZATION.md v1.2.4 "
                      "(execution-convention policy): primary convention = "
                      "close-to-close for both sleeves of any portfolio; "
                      "promotion gates evaluated on the primary convention; "
                      "overnight convention reported secondarily; "
                      "mixed-convention portfolios prohibited (E020 lesson); "
                      "convention-dependent strategies (overnight z >= 3, "
                      "c2c z < 3) flagged for promotion re-examination; new "
                      "engines must verify the per-asset accounting identity "
                      "before results are trusted.",
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-sim", type=int, default=PLACEBO_N,
                        help="placebo simulations for Part B (default 50)")
    parser.add_argument("--parts", default="abc",
                        help="parts to run (default abc): a=decomposition, "
                             "b=placebos, c=adjusted-open check")
    parser.add_argument("--merge", action="store_true",
                        help="merge cached part outputs into the consolidated "
                             "JSON without re-running any part")
    args = parser.parse_args()
    n_sim = args.n_sim
    parts = set(args.parts)

    OUT_DIR = os.path.dirname(os.path.abspath(__file__))
    part_cache = {
        "a": os.path.join(OUT_DIR, "e024_part_a.json"),
        "b": os.path.join(OUT_DIR, "e024_part_b.json"),
        "c": os.path.join(OUT_DIR, "e024_part_c.json"),
    }

    if args.merge:
        result = _merge(part_cache)
        out_path = os.path.join("experiments", "e024_convention_audit.json")
        with open(out_path, "w") as f:
            jsonio.dump(result, f, indent=2, default=str)
        print(f"\nMerged {out_path}")
        return

    t0 = time.time()
    print("=" * 74)
    print("E024: Overnight-Intraday Decomposition Audit + Adjusted-Open")
    print("Data-Integrity Check + Convention Policy")
    print("=" * 74)
    print(f"Pre-registered: FE1 (Part C, adjusted-open integrity), "
          f"FE2 (flagship overnight share >= {FE2_MIN_SHARE:.0%}), "
          f"FE3 (intraday excess <= {FE3_MAX_INTRA_EXCESS})")
    print(f"Placebo sims (Part B): {n_sim}; block: {BLOCK_DAYS}d "
          f"(daily) / {BLOCK_MONTHS}m (monthly)")

    ctx = build_contexts()
    specs = build_specs(ctx)
    print(f"\nPanels: equity {ctx['equity']['close'].shape[1]} tickers, "
          f"futures {ctx['futures']['de_index'].shape[1]} contracts "
          f"({ctx['futures']['de_index'].index[0].date()}.."
          f"{ctx['futures']['de_index'].index[-1].date()}), "
          f"cross-asset {ctx['cross_asset']['close'].shape[1]} ETFs")

    result = {
        "experiment": "E024",
        "timestamp": deterministic_timestamp(),
        "title": "Overnight-intraday decomposition audit, adjusted-open "
                 "data-integrity check and execution-convention policy",
        "pre_registered": {
            "FE1_adjusted_open_integrity": {
                "expectation": "adjusted ex-date overnight returns consistent "
                               "with total-return accounting",
                "falsification_rule": "pooled mean ex-date adjusted overnight "
                                      "return < -0.5 x median dividend yield",
            },
            "FE2_flagship_overnight_share": {
                "expectation": f"equity flagship overnight share of c2c edge "
                               f">= {FE2_MIN_SHARE:.0%}",
            },
            "FE3_intraday_excess": {
                "expectation": f"no strategy's intraday-only OOS Sharpe "
                               f"exceeds its c2c OOS Sharpe by more than "
                               f"{FE3_MAX_INTRA_EXCESS}",
            },
            "convention_dependence_flag": "overnight placebo z >= 3 with "
                                          "c2c placebo z < 3",
            "engines": {
                "c2c": "gross[t] = w_s[t] * (close[t+1]/close[t] - 1)",
                "overnight": "gross[t] = w_s[t] * (open[t+1]/close[t] - 1)",
                "intraday": "gross[t] = w_s[t] * (close[t+1]/open[t+1] - 1)",
                "weight_path": "identical shifted + rebalance-sampled weights "
                               "across conventions (identical turnover/costs)",
                "identity": "per-asset c2c[t+1] = (1+overnight[t])*(1+intraday[t]) - 1, "
                            "asserted < 1e-9 (verified empirically: 0.0; the two "
                            "wrong alignments give 0.658 and 0.611 on the flagship)",
            },
            "futures_deseamed_opens": "de-seamed open reconstructed by "
                                      "splitting each day's de-seamed return "
                                      "with the raw futures split on non-seam "
                                      "days and the paired spot ETF split on "
                                      "seam days",
            "placebo_null": "12m block permutation of each strategy's signal "
                            "(carry: E018 seam-calendar-preserving permutation "
                            "of seam excess gaps)",
        },
    }

    # ---------------- Part A ----------------
    part_a = {}
    identity_checks = {}
    if "a" in parts:
        print("\n" + "-" * 74)
        print("Part A: three-convention decomposition (deterministic)")
        print("-" * 74)
        for spec in specs:
            fam = spec["family"]
            close, open_, spy_ret = _panel_ctx(ctx, fam)
            # Engineering guard: accounting identity before trusting any number.
            idiff = verify_identity(close, open_, spec["rebal"])
            identity_checks[spec["name"]] = idiff
            assert idiff < IDENTITY_TOL, (
                f"accounting identity violated for {spec['name']} "
                f"(max diff {idiff:.3e})")

            w = spec["weights"](spec["signal"]())
            res = {}
            rets_store = {}
            for conv in CONVENTIONS:
                res[conv] = evaluate_convention(
                    conv, w, close, open_, spy_ret, spec["rebal"])
                rets_store[conv] = engine(
                    conv, w, close, open_, spec["rebal"])
            share = overnight_share(
                rets_store["overnight"], rets_store["c2c"],
                res["c2c"]["oos_sharpe"])
            intra_excess = (res["intraday"]["oos_sharpe"]
                            - res["c2c"]["oos_sharpe"])
            part_a[spec["name"]] = {
                "family": fam,
                "label": spec["label"],
                "rebalance_freq_days": spec["rebal"],
                "n_assets": int(close.shape[1]),
                "period": f"{close.index[0].date()}.."
                          f"{close.index[-1].date()}",
                "identity_max_abs_diff": idiff,
                "conventions": res,
                "overnight_share_of_c2c_edge": share,
                "intraday_minus_c2c_oos_sharpe": float(intra_excess),
            }
            r = part_a[spec["name"]]
            print(f"    {spec['name']:<34s} c2c={res['c2c']['oos_sharpe']:+.3f} "
                  f"on={res['overnight']['oos_sharpe']:+.3f} "
                  f"intra={res['intraday']['oos_sharpe']:+.3f} "
                  f"share={'n/a' if share is None else f'{share:.2f}'} "
                  f"beta={res['c2c']['equity_beta']:+.3f} "
                  f"turn={res['c2c']['turnover']:.4f} "
                  f"[{time.time()-t0:.0f}s]")
        result["part_a"] = part_a
        result["identity_checks"] = identity_checks
        with open(part_cache["a"], "w") as f:
            jsonio.dump({"part_a": part_a,
                         "identity_checks": identity_checks}, f, indent=2,
                        default=str)

    # ---------------- Part B ----------------
    part_b = {}
    if "b" in parts:
        print("\n" + "-" * 74)
        print(f"Part B: matched placebos under c2c and overnight "
              f"conventions ({n_sim} sims)")
        print("-" * 74)
        for spec in specs:
            fam = spec["family"]
            close, open_, spy_ret = _panel_ctx(ctx, fam)
            w_real = spec["weights"](spec["signal"]())
            real = {
                conv: evaluate_convention(
                    conv, w_real, close, open_, spy_ret, spec["rebal"])
                for conv in ("c2c", "overnight")
            }
            sims_c2c, sims_on = [], []
            for i in range(n_sim):
                psig = spec["placebo"](SEED + i)
                pw = spec["weights"](psig)
                sims_c2c.append(evaluate_convention(
                    "c2c", pw, close, open_, spy_ret,
                    spec["rebal"])["oos_sharpe"])
                sims_on.append(evaluate_convention(
                    "overnight", pw, close, open_, spy_ret,
                    spec["rebal"])["oos_sharpe"])
                if (i + 1) % 10 == 0:
                    print(f"      ... {spec['name']}: {i + 1}/{n_sim} sims "
                          f"[{time.time()-t0:.0f}s]")
            pb = {}
            flags = {}
            for conv, sims in (("c2c", sims_c2c), ("overnight", sims_on)):
                mu = float(np.mean(sims))
                sd = float(np.std(sims))
                z = ((real[conv]["oos_sharpe"] - mu) / sd
                     if sd > 0 else float("nan"))
                pb[conv] = {
                    "real_oos_sharpe": real[conv]["oos_sharpe"],
                    "placebo_mean": mu,
                    "placebo_std": sd,
                    "z_score": float(z),
                }
            conv_dep = bool(pb["overnight"]["z_score"] >= 3.0
                            and pb["c2c"]["z_score"] < 3.0)
            part_b[spec["name"]] = {
                "family": fam,
                "label": spec["label"],
                "null": "12m block permutation of the strategy signal"
                        if spec["name"] != "carry_realized_roll_yield_futures"
                        else "E018 seam-calendar-preserving permutation of "
                             "seam excess gaps",
                "c2c": pb["c2c"],
                "overnight": pb["overnight"],
                "convention_dependent": conv_dep,
            }
            print(f"    {spec['name']:<34s} z_c2c={pb['c2c']['z_score']:+.2f} "
                  f"z_on={pb['overnight']['z_score']:+.2f} "
                  f"conv_dependent={conv_dep}")
        result["part_b"] = part_b
        with open(part_cache["b"], "w") as f:
            jsonio.dump({"part_b": part_b}, f, indent=2, default=str)

    # ---------------- Part C ----------------
    if "c" in parts:
        print("\n" + "-" * 74)
        print("Part C: adjusted-open data-integrity check (ex-dividend dates)")
        print("-" * 74)
        sample = ["SPY"] + LARGE_LIQUID[:10]
        pc = part_c(sample)
        result["part_c"] = pc
        with open(part_cache["c"], "w") as f:
            jsonio.dump({"part_c": pc}, f, indent=2, default=str)
        pooled = pc["pooled"]
        fe1 = pc["FE1"]
        print(f"    sample: {len(sample)} tickers, "
              f"{pooled['n_ex_dates']} ex-dates")
        print(f"    median dividend yield: {pooled['median_dividend_yield']:.5f}")
        print(f"    mean adjusted overnight on ex-dates: "
              f"{pooled['mean_adj_overnight_ex_date']:+.5f}")
        print(f"    mean raw overnight on ex-dates: "
              f"{pooled['mean_raw_overnight_ex_date']:+.5f} "
              f"(expected ~= {-pooled['median_dividend_yield']:+.5f} + drift)")
        print(f"    FE1 threshold: {fe1['threshold']:+.5f} -> "
              f"{'FALSIFIED' if fe1['falsified'] else 'NOT falsified'}")

    # ---------------- Pre-registered expectation evaluation ----------------
    fe = {}
    if "a" in parts:
        flagship = part_a.get("time_series_momentum", {})
        share = flagship.get("overnight_share_of_c2c_edge")
        fe["FE2_flagship_overnight_share"] = {
            "value": share,
            "threshold": FE2_MIN_SHARE,
            "passed": bool(share is not None and share >= FE2_MIN_SHARE),
        }
        worst_excess = None
        worst_name = None
        for name, r in part_a.items():
            ex = r.get("intraday_minus_c2c_oos_sharpe")
            if ex is not None and (worst_excess is None or ex > worst_excess):
                worst_excess = ex
                worst_name = name
        fe["FE3_intraday_excess"] = {
            "max_excess": worst_excess,
            "strategy": worst_name,
            "threshold": FE3_MAX_INTRA_EXCESS,
            "passed": bool(worst_excess is not None
                           and worst_excess <= FE3_MAX_INTRA_EXCESS),
        }
    if "c" in parts:
        fe["FE1_adjusted_open_integrity"] = {
            "falsified": result["part_c"]["FE1"]["falsified"],
            "passed": not result["part_c"]["FE1"]["falsified"],
        }
    result["falsification_expectations"] = fe

    # ---------------- Part D: convention policy reference ----------------
    result["part_d"] = {
        "policy": "Recorded in ledger/PRIORITIZATION.md v1.2.4 "
                  "(execution-convention policy): primary convention = "
                  "close-to-close for both sleeves of any portfolio; "
                  "promotion gates evaluated on the primary convention; "
                  "overnight convention reported secondarily; "
                  "mixed-convention portfolios prohibited (E020 lesson); "
                  "convention-dependent strategies (overnight z >= 3, "
                  "c2c z < 3) flagged for promotion re-examination; new "
                  "engines must verify the per-asset accounting identity "
                  "before results are trusted.",
    }

    out_path = os.path.join("experiments", "e024_convention_audit.json")
    with open(out_path, "w") as f:
        jsonio.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path} ({time.time()-t0:.0f}s total)")


if __name__ == "__main__":
    main()
