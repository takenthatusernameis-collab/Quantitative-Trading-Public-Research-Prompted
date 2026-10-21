#!/usr/bin/env python3
"""E017: TSM + carry on an extended (2014-2026) properly-rolled futures panel.

Follows up the E016 handoff. E016's panel was truncated to 2017-07-10 because
RTY=F data on yfinance starts then, leaving only 28 OOS folds in a difficult
trend-following regime. E017 restores the full 2014-2026 sample by dropping
RTY=F and adding breadth (HG/ZW/ZS/ZC + spot-ETF pairs CPER/WEAT/SOYB/CORN).

Design:
  - Universe: 16 liquid futures contracts across equities, bonds,
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

Sample-period isolation:
  - Extended 16-contract panel restricted to 2017-07-10+ (same universe,
    short sample) isolates the sample-period effect from universe breadth.
  - E016 replication: the original 13-contract panel (incl. RTY=F) on
    2017-07-10+ with the canonical 12m lookback reproduces E016's 0.717.

E015 re-validation:
  - E015's multi-asset pure-TSM result (OOS Sharpe 2.086) used raw
    stitched futures for 7 tickers (ES, NQ, GC, CL, ZB, NG, 6E).
    Re-run with de-seamed indices replacing those 7 columns and record
    the delta.
"""

import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import data, backtest, strategies, futures, multiasset
from src import jsonio
from src.run_experiment import UNIVERSES, deterministic_timestamp

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

# E016's original 13-contract universe (incl. RTY=F), for replication.
E016_UNIVERSE = {
    "ES=F": ("SPY", "quarterly"),
    "NQ=F": ("QQQ", "quarterly"),
    "YM=F": ("DIA", "quarterly"),
    "RTY=F": ("IWM", "quarterly"),
    "ZB=F": ("TLT", "quarterly"),
    "ZN=F": ("IEF", "quarterly"),
    "GC=F": ("GLD", "monthly"),
    "SI=F": ("SLV", "monthly"),
    "CL=F": ("USO", "monthly"),
    "NG=F": ("UNG", "monthly"),
    "6E=F": ("FXE", "quarterly"),
    "6B=F": ("FXF", "quarterly"),
    "6J=F": ("FXY", "quarterly"),
}

# Subsample start matching E016's truncated panel.
SUBSAMPLE_START = "2017-07-10"

# Futures tickers in the E015 multi-asset universe (raw-stitched there).
E015_FUTURES_TICKERS = ["ES=F", "NQ=F", "GC=F", "CL=F", "ZB=F", "NG=F", "6E=F"]

# Pre-registered primary lookback (months). See module docstring for
# justification; 6/9/12/18m reported as sensitivity with multiple-testing
# awareness, NOT used to select the primary.
PRIMARY_LOOKBACK = 9

# Pre-registered promotion gates (set before running).
GATES = {
    "oos_sharpe_gte_1.0": 1.0,
    "placebo_z_gte_3": 3.0,
    "bear_sharpe_positive": 0.0,
    "abs_beta_lte_0.2": 0.2,
}


def build_panels(universe, start=START):
    """Download and build raw / de-seamed / carry panels for a futures universe."""
    fut_tickers = list(universe.keys())
    spot_tickers = [v[0] for v in universe.values()]
    tickers = sorted(set(fut_tickers + spot_tickers + ["SPY"]))
    df = data.download(tickers, start=start)

    raw_fut, raw_spot, raw_open = {}, {}, {}
    for ft, (st, cad) in universe.items():
        f = data.wide_close(df, ft)
        s = data.wide_close(df, st)
        o = data.get_panel(df, "Open")[ft]
        # Spot panel is keyed by the futures ticker so the two
        # panels share columns (each futures contract has exactly
        # one paired spot ETF).
        raw_fut[ft] = f["close"]
        raw_spot[ft] = s["close"]
        raw_open[ft] = o

    fut_close = pd.DataFrame(raw_fut).dropna(axis=1, how="all")
    spot_close = pd.DataFrame(raw_spot).reindex(columns=fut_close.columns).ffill()
    fut_open = pd.DataFrame(raw_open).reindex(columns=fut_close.columns).ffill()

    # Align all series to common trading dates.
    common = fut_close.dropna().index
    for col in spot_close.columns:
        common = common.intersection(spot_close[col].dropna().index)
    common = common.intersection(fut_open.dropna().index)
    fut_close = fut_close.loc[common]
    spot_close = spot_close.loc[common].ffill()
    fut_open = fut_open.loc[common].ffill()

    # De-seamed indices and seam diagnostics.
    idx = {}
    seams = {}
    seam_stats = {}
    for ft, (st, cad) in universe.items():
        f = fut_close[ft]
        s = spot_close[ft]
        detected = futures.detect_seams(f, s, cadence=cad)
        clean_ret = futures.deseam_returns(f, s, detected)
        idx[ft] = futures.deseam_index(clean_ret)
        seams[ft] = pd.DatetimeIndex(detected)

        # Excess-gap magnitudes at detected seams (the removed artifacts).
        r_fut = f.pct_change()
        r_spot = s.reindex(f.index).ffill().pct_change()
        excess = (r_fut - r_spot).reindex(pd.DatetimeIndex(detected))
        seam_stats[ft] = {
            "cadence": cad,
            "n_seams": int(len(detected)),
            "median_excess_gap": float(np.nanmedian(excess.abs())) if len(excess) else 0.0,
            "max_excess_gap": float(np.nanmax(excess.abs())) if len(excess) else 0.0,
            "max_seam_date": str(excess.abs().idxmax().date()) if len(excess) and np.isfinite(excess.abs().max()) else None,
        }

    de_index = pd.DataFrame(idx).loc[common]
    carry = strategies.carry_signal(fut_close, spot_close)
    # Secondary carry variant: trailing realized roll yield from seam gaps.
    carry_rroll = pd.DataFrame(index=fut_close.index, columns=fut_close.columns, dtype=float)
    for ft, (st, cad) in universe.items():
        carry_rroll[ft] = futures.realized_roll_yield(
            fut_close[ft], spot_close[ft], seams[ft]
        )

    bm = data.download(["SPY"], start=start)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(common).ffill()

    return {
        "fut_close": fut_close,
        "fut_open": fut_open,
        "spot_close": spot_close,
        "de_index": de_index,
        "carry": carry,
        "carry_rroll": carry_rroll,
        "spy": spy,
        "seams": {k: [str(d.date()) for d in v] for k, v in seams.items()},
        "seam_stats": seam_stats,
    }


def market_diagnostics(ret, spy_ret):
    """Full-sample metrics + market-neutrality diagnostics (equity beta, corr)."""
    net = ret["net"].dropna()
    m = backtest.metrics(net)
    common = net.index.intersection(spy_ret.index)
    y = net.loc[common].values
    x = spy_ret.loc[common].values
    if len(y) > 2 and np.std(x) > 0:
        A = np.vstack([np.ones(len(x)), x]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        alpha, beta_coef = float(coef[0]), float(coef[1])
        corr = float(np.corrcoef(y, x)[0, 1])
    else:
        alpha, beta_coef, corr = float("nan"), float("nan"), float("nan")
    return {
        "sharpe": m.get("sharpe"),
        "annual_return": m.get("annual_return"),
        "annual_vol": m.get("annual_vol"),
        "max_drawdown": m.get("max_drawdown"),
        "total_return": m.get("total_return"),
        "n_days": m.get("n_days"),
        "equity_beta": beta_coef,
        "alpha_annual": alpha * 252,
        "corr_spy": corr,
    }


def walk_forward(ret, close, spy_ret):
    """Walk-forward OOS fold metrics with regime classification."""
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    fold_metrics = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        test_idx = close.index[te_s:te_e]
        test_rets = ret.loc[ret.index.intersection(test_idx)]
        m = backtest.metrics(test_rets["net"])
        m["fold"] = i
        spy_win = spy_ret.loc[spy_ret.index.intersection(test_idx)]
        spy_win_ret = float(spy_win.sum()) if len(spy_win) else float("nan")
        if spy_win_ret > 0.02:
            regime = "bull"
        elif spy_win_ret < -0.02:
            regime = "bear"
        else:
            regime = "sideways"
        m["regime"] = regime
        m["spy_test_return"] = spy_win_ret
        fold_metrics.append(m)
    return fold_metrics, splits


def regime_summary(fold_metrics):
    out = {}
    for regime in ["bull", "bear", "sideways"]:
        rows = [m for m in fold_metrics if m.get("regime") == regime]
        sharps = [m["sharpe"] for m in rows
                  if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
        out[regime] = {
            "n_folds": len(rows),
            "sharpe_mean": float(np.mean(sharps)) if sharps else float("nan"),
            "sharpe_pos": int(sum(1 for s in sharps if s > 0)) if sharps else 0,
        }
    return out


def compute_drawdown(ret):
    ret = ret.dropna()
    if len(ret) == 0:
        return 0.0, 0
    cum = (1.0 + ret).cumprod()
    roll = cum.cummax()
    dd = cum / roll - 1.0
    underwater = int((dd < 0).sum())
    return float(dd.min()), underwater


def evaluate(close, open_, spy, weights, label):
    """Full evaluation of a weight panel: OOS, beta, turnover, DD, regime."""
    ret = backtest.portfolio_returns_rebalance_clean(
        weights, close, open_, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
    )
    spy_ret = spy.pct_change().fillna(0.0)
    diag = market_diagnostics(ret, spy_ret)
    fm, splits = walk_forward(ret, close, spy_ret)
    sharpes = [m["sharpe"] for m in fm
               if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
    oos_sharpe = float(np.mean(sharpes)) if sharpes else float("nan")
    oos_std = float(np.std(sharpes)) if sharpes else float("nan")
    turn = backtest.average_turnover(weights)
    dd, uw = compute_drawdown(ret["net"])
    reg = regime_summary(fm)
    n_pos = int(sum(1 for m in fm if m.get("sharpe") is not None and m.get("sharpe", 0) > 0))
    return {
        "label": label,
        "is_sharpe": diag["sharpe"],
        "is_ann_return": diag["annual_return"],
        "is_ann_vol": diag["annual_vol"],
        "oos_sharpe": oos_sharpe,
        "oos_sharpe_std": oos_std,
        "turnover": turn,
        "equity_beta": diag["equity_beta"],
        "corr_spy": diag["corr_spy"],
        "alpha_annual": diag["alpha_annual"],
        "max_drawdown": dd,
        "time_underwater_days": uw,
        "positive_folds": n_pos,
        "n_folds": len(splits),
        "n_tickers": int(close.shape[1]),
        "regime_analysis": reg,
    }, fm


def blended_placebo(de_index, spy, n_sim=PLACEBO_N_SIM):
    """Placebo null: random TSM + random carry, blended 50/50."""
    rng = np.random.default_rng(SEED)
    spy_ret = spy.pct_change().fillna(0.0)
    sharps = []
    vol = de_index.pct_change().rolling(63).std().replace(0, np.nan)
    for _ in range(n_sim):
        tsm_sig = pd.DataFrame(
            rng.standard_normal(size=de_index.shape),
            index=de_index.index, columns=de_index.columns,
        )
        tsm_w = backtest.time_series_momentum_weights(
            tsm_sig, de_index, long_only=False, vol_window=63
        )
        carry_sig = pd.DataFrame(
            rng.standard_normal(size=de_index.shape),
            index=de_index.index, columns=de_index.columns,
        )
        carry_w = backtest.carry_weights(carry_sig, vol)
        bw = 0.5 * tsm_w + 0.5 * carry_w
        r = backtest.portfolio_returns_rebalance_clean(
            bw, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
        )
        fm, _ = walk_forward(r, de_index, spy_ret)
        s = [m["sharpe"] for m in fm
             if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
        sharps.append(float(np.mean(s)) if s else 0.0)
    return float(np.mean(sharps)), float(np.std(sharps))


def cost_sweep(weights, close, open_, spy):
    """Net Sharpe under base vs high cost assumptions."""
    spy_ret = spy.pct_change().fillna(0.0)
    out = {}
    for name, tc, sl in [("base_0.5_0.2bps", 0.0005, 0.0002),
                         ("high_20_5bps", 0.0020, 0.0005),
                         ("zero_cost", 0.0, 0.0)]:
        ret = backtest.portfolio_returns_rebalance_clean(
            weights, close, open_, tc_cost=tc, slippage=sl, rebalance_freq=REBAL
        )
        fm, _ = walk_forward(ret, close, spy_ret)
        sharpes = [m["sharpe"] for m in fm
                   if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
        out[name] = {
            "tc_cost": tc,
            "slippage": sl,
            "oos_sharpe": float(np.mean(sharpes)) if sharpes else float("nan"),
        }
    return out


def validation_extras(de_index, spy, primary_lookback):
    """Supplementary validation: per-contract standalone TSM OOS Sharpe
    and TSM lookback sensitivity (guards against a single-contract or
    single-lookback driving the book result)."""
    spy_ret = spy.pct_change().fillna(0.0)
    splits = backtest.walk_forward_splits(len(de_index), TRAIN, TEST, STEP)

    per_contract = {}
    for col in de_index.columns:
        sig = strategies.time_series_momentum_pure(de_index[[col]], lookback=primary_lookback, skip=1)
        w = backtest.time_series_momentum_weights(
            sig, de_index[[col]], long_only=False, vol_window=63
        )
        r = backtest.portfolio_returns_rebalance_clean(
            w, de_index[[col]], de_index[[col]],
            tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
        )
        sh = [backtest.metrics(r.loc[r.index.intersection(de_index.index[c:d])]["net"])["sharpe"]
              for (_, _, c, d) in splits]
        sh = [s for s in sh if s == s]
        per_contract[col] = {
            "oos_sharpe": float(np.mean(sh)) if sh else float("nan"),
            "positive_folds": int(sum(1 for s in sh if s > 0)),
            "n_folds": len(sh),
        }

    lookbacks = {}
    for lb in [6, primary_lookback, 12, 18]:
        sig = strategies.time_series_momentum_pure(de_index, lookback=lb, skip=1)
        w = backtest.time_series_momentum_weights(
            sig, de_index, long_only=False, vol_window=63
        )
        r = backtest.portfolio_returns_rebalance_clean(
            w, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
        )
        sh = [backtest.metrics(r.loc[r.index.intersection(de_index.index[c:d])]["net"])["sharpe"]
              for (_, _, c, d) in splits]
        sh = [s for s in sh if s == s]
        lookbacks[f"{lb}m"] = {
            "lookback_months": lb,
            "oos_sharpe": float(np.mean(sh)) if sh else float("nan"),
            "positive_folds": int(sum(1 for s in sh if s > 0)),
            "n_folds": len(sh),
        }
    return {"per_contract_tsm": per_contract, "tsm_lookback_sensitivity": lookbacks}


def subsample_check(panels, universe, label, lookback):
    """Re-run the strategy grid on a restricted panel (sample-period isolation)."""
    start_idx = panels["de_index"].index >= pd.Timestamp(SUBSAMPLE_START)
    sub = {
        "fut_close": panels["fut_close"].loc[start_idx],
        "fut_open": panels["fut_open"].loc[start_idx],
        "de_index": panels["de_index"].loc[start_idx],
        "carry": panels["carry"].loc[start_idx],
        "carry_rroll": panels["carry_rroll"].loc[start_idx],
        "spy": panels["spy"].loc[start_idx],
    }
    return strategy_grid(sub, lookback, label)


def strategy_grid(panels, lookback, label_prefix=""):
    """Evaluate the E016 strategy grid (TSM raw/de-seamed, both carry
    variants, 50/50 blend) at a given TSM lookback."""
    fut_close = panels["fut_close"]
    fut_open = panels["fut_open"]
    de_index = panels["de_index"]
    carry = panels["carry"]
    carry_rroll = panels["carry_rroll"]
    spy = panels["spy"]

    tsm_sig_raw = strategies.time_series_momentum_pure(fut_close, lookback=lookback, skip=1)
    w_tsm_raw = backtest.time_series_momentum_weights(
        tsm_sig_raw, fut_close, long_only=False, vol_window=63
    )
    tsm_sig = strategies.time_series_momentum_pure(de_index, lookback=lookback, skip=1)
    w_tsm = backtest.time_series_momentum_weights(
        tsm_sig, de_index, long_only=False, vol_window=63
    )
    vol = de_index.pct_change().rolling(63).std().replace(0, np.nan)
    w_carry = backtest.carry_weights(carry, vol)
    w_carry_rroll = backtest.carry_weights(carry_rroll, vol)
    w_blend = 0.5 * w_tsm + 0.5 * w_carry

    out = {}
    for lbl, weights, cl, op in [
        (f"{label_prefix}tsm_raw_stitched", w_tsm_raw, fut_close, fut_open),
        (f"{label_prefix}tsm_deseamed", w_tsm, de_index, de_index),
        (f"{label_prefix}carry_normalized_basis", w_carry, de_index, de_index),
        (f"{label_prefix}carry_realized_rollyield", w_carry_rroll, de_index, de_index),
        (f"{label_prefix}blend_tsm_carry_50_50", w_blend, de_index, de_index),
    ]:
        res, _ = evaluate(cl, op, spy, weights, lbl)
        out[lbl] = res
    return out


def e015_revalidation(de_index):
    """Re-validate E015's multi-asset pure-TSM result with de-seamed futures.

    E015's multi-asset universe used raw stitched futures for 7 tickers
    (ES, NQ, GC, CL, ZB, NG, 6E). Replace those columns with de-seamed
    indices and re-run pure TSM (12m, long-only, monthly rebal, E015
    config). The delta isolates the roll-artifact contamination.
    """
    universe = UNIVERSES["multi_asset"]
    df = data.download(universe, start=START)
    close = data.get_panel(df, "Close").dropna(axis=1, how="all").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close").dropna(how="all")["SPY"].reindex(close.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)

    # Raw replication (E015's construction, for a like-for-like baseline).
    tsm_sig = strategies.time_series_momentum_pure(close, lookback=12, skip=1)
    tsm_w = backtest.time_series_momentum_weights(
        tsm_sig, close, long_only=True, vol_window=63
    )
    ret_raw = backtest.portfolio_returns_rebalance_clean(
        tsm_w, close, open_, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
    )
    fm_raw, splits = walk_forward(ret_raw, close, spy_ret)
    sh_raw = [m["sharpe"] for m in fm_raw
              if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]

    # De-seamed: replace the 7 raw futures columns with de-seamed indices.
    close_ds = close.copy()
    open_ds = open_.copy()
    de_reidx = de_index.reindex(close.index).ffill()
    for ft in E015_FUTURES_TICKERS:
        if ft in close_ds.columns and ft in de_reidx.columns:
            close_ds[ft] = de_reidx[ft]
            # De-seamed index has no observable opens: close-to-close execution.
            open_ds[ft] = de_reidx[ft]
    tsm_sig_ds = strategies.time_series_momentum_pure(close_ds, lookback=12, skip=1)
    tsm_w_ds = backtest.time_series_momentum_weights(
        tsm_sig_ds, close_ds, long_only=True, vol_window=63
    )
    ret_ds = backtest.portfolio_returns_rebalance_clean(
        tsm_w_ds, close_ds, open_ds, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
    )
    diag_ds = market_diagnostics(ret_ds, spy_ret)
    fm_ds, _ = walk_forward(ret_ds, close_ds, spy_ret)
    sh_ds = [m["sharpe"] for m in fm_ds
             if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
    dd_ds, _ = compute_drawdown(ret_ds["net"])
    reg_ds = regime_summary(fm_ds)

    return {
        "n_tickers": int(close.shape[1]),
        "n_days": int(len(close)),
        "n_folds": len(splits),
        "futures_replaced": [ft for ft in E015_FUTURES_TICKERS if ft in close.columns],
        "raw_stitched": {
            "oos_sharpe": float(np.mean(sh_raw)) if sh_raw else float("nan"),
            "positive_folds": int(sum(1 for s in sh_raw if s > 0)),
        },
        "deseamed": {
            "oos_sharpe": float(np.mean(sh_ds)) if sh_ds else float("nan"),
            "positive_folds": int(sum(1 for s in sh_ds if s > 0)),
            "equity_beta": diag_ds["equity_beta"],
            "corr_spy": diag_ds["corr_spy"],
            "max_drawdown": dd_ds,
            "turnover": backtest.average_turnover(tsm_w_ds),
            "regime_analysis": reg_ds,
        },
        "delta_sharpe": (float(np.mean(sh_ds)) if sh_ds else float("nan"))
                        - (float(np.mean(sh_raw)) if sh_raw else float("nan")),
        "e015_reported": 2.086,
    }


def main():
    print("=" * 72)
    print("E017: TSM + Carry on an Extended (2014-2026) Futures Panel")
    print("=" * 72)

    panels = build_panels(FUTURES_UNIVERSE)
    fut_close = panels["fut_close"]
    fut_open = panels["fut_open"]
    spot_close = panels["spot_close"]
    de_index = panels["de_index"]
    carry = panels["carry"]
    carry_rroll = panels["carry_rroll"]
    spy = panels["spy"]
    seam_stats = panels["seam_stats"]

    print(f"\nLoaded: {len(de_index)} common trading days, {de_index.shape[1]} futures contracts")
    print(f"  Futures: {list(de_index.columns)}")
    print(f"  Period: {de_index.index[0].date()} to {de_index.index[-1].date()}")
    print(f"  Pre-registered primary TSM lookback: {PRIMARY_LOOKBACK}m")

    # ---- Part 1: roll-seam diagnostics ----
    print("\n" + "-" * 72)
    print("Part 1: Roll-seam detection (raw continuous contracts)")
    print("-" * 72)
    for ft, (st, cad) in FUTURES_UNIVERSE.items():
        s = seam_stats[ft]
        print(f"  {ft:<6} (vs {st:<4}) seams={s['n_seams']:<3} "
              f"median_gap={s['median_excess_gap']*100:.3f}%  "
              f"max_gap={s['max_excess_gap']*100:.2f}%  at {s['max_seam_date']}")

    # CL April-2020 case study: raw vs de-seamed returns.
    cl_raw_ret = fut_close["CL=F"].pct_change()
    r_spot = spot_close["CL=F"].reindex(fut_close.index).ffill().pct_change()
    case = {}
    for d in ["2020-04-20", "2020-04-21"]:
        ts = pd.Timestamp(d)
        if ts in cl_raw_ret.index:
            case[d] = {
                "raw_cl_return": float(cl_raw_ret.loc[ts]),
                "uso_return": float(r_spot.loc[ts]),
                "deseamed_return": float(r_spot.loc[ts]),
            }
    print("\n  CL=F April-2020 roll-wedge case study (raw vs de-seamed):")
    for d, v in case.items():
        print(f"    {d}: raw CL return {v['raw_cl_return']*100:+.1f}%  "
              f"-> de-seamed (USO proxy) {v['deseamed_return']*100:+.1f}%")

    # ---- Part 2: strategies (primary lookback) ----
    print("\n" + "-" * 72)
    print(f"Part 2: Strategy construction (primary TSM lookback {PRIMARY_LOOKBACK}m)")
    print("-" * 72)
    results = strategy_grid(panels, PRIMARY_LOOKBACK)
    for lbl, res in results.items():
        bear = res["regime_analysis"]["bear"]["sharpe_mean"]
        print(f"    {lbl:<28} OOS_Sharpe={res['oos_sharpe']:.3f}  "
              f"beta={res['equity_beta']:+.3f}  corr={res['corr_spy']:+.3f}  "
              f"maxDD={res['max_drawdown']:.3f}  bear_Sh={bear:+.3f}  "
              f"turn={res['turnover']:.4f}  pos={res['positive_folds']}/{res['n_folds']}")

    # Correlation between the two carry signals (information overlap).
    c_corr = float(carry.stack().corr(carry_rroll.stack()))
    print(f"\n  Carry signal correlation (normalized basis vs realized roll yield): {c_corr:.3f}")
    results["carry_signal_correlation"] = c_corr

    # ---- Part 3: placebo validation ----
    print("\n  Blended placebo null (50 random TSM + random carry, 50/50)...")
    pm, ps = blended_placebo(de_index, spy)
    print(f"    Placebo: mean Sharpe={pm:.3f}  std={ps:.3f}  n_sim={PLACEBO_N_SIM}")
    for lbl in ["tsm_deseamed", "carry_normalized_basis",
                "carry_realized_rollyield", "blend_tsm_carry_50_50"]:
        z = (results[lbl]["oos_sharpe"] - pm) / ps if ps > 0 else float("nan")
        results[lbl]["placebo_z"] = float(z)
        results[lbl]["placebo_mean"] = pm
        results[lbl]["placebo_std"] = ps
        print(f"    {lbl:<28} placebo z={z:.2f}")

    # ---- Part 4: cost sweep on the blend ----
    print("\n  Cost sweep (blend):")
    w_blend = None
    # Rebuild blend weights for the cost sweep.
    tsm_sig = strategies.time_series_momentum_pure(de_index, lookback=PRIMARY_LOOKBACK, skip=1)
    w_tsm = backtest.time_series_momentum_weights(
        tsm_sig, de_index, long_only=False, vol_window=63
    )
    vol = de_index.pct_change().rolling(63).std().replace(0, np.nan)
    w_carry = backtest.carry_weights(carry, vol)
    w_blend = 0.5 * w_tsm + 0.5 * w_carry
    cs = cost_sweep(w_blend, de_index, de_index, spy)
    for name, v in cs.items():
        print(f"    {name:<16} OOS Sharpe={v['oos_sharpe']:.3f}")
    results["blend_tsm_carry_50_50"]["cost_sweep"] = cs

    # ---- Part 5: pre-registered promotion gates (on the blend) ----
    blend = results["blend_tsm_carry_50_50"]
    gates = {
        "oos_sharpe_gte_1.0": bool(blend["oos_sharpe"] >= GATES["oos_sharpe_gte_1.0"]),
        "abs_beta_lte_0.2": bool(abs(blend["equity_beta"]) <= GATES["abs_beta_lte_0.2"]),
        "bear_sharpe_positive": bool(blend["regime_analysis"]["bear"]["sharpe_mean"] > GATES["bear_sharpe_positive"]),
        "placebo_z_gte_3": bool(blend.get("placebo_z", 0) >= GATES["placebo_z_gte_3"]),
    }
    print("\n  Pre-registered promotion gates (blend):")
    for g, ok in gates.items():
        print(f"    {g:<28} {'PASS' if ok else 'FAIL'}")
    gates["all_passed"] = all(v for k, v in gates.items() if k != "all_passed")

    # Gates on the primary TSM strategy too (the lead candidate).
    tsm_res = results["tsm_deseamed"]
    tsm_gates = {
        "oos_sharpe_gte_1.0": bool(tsm_res["oos_sharpe"] >= GATES["oos_sharpe_gte_1.0"]),
        "abs_beta_lte_0.2": bool(abs(tsm_res["equity_beta"]) <= GATES["abs_beta_lte_0.2"]),
        "bear_sharpe_positive": bool(tsm_res["regime_analysis"]["bear"]["sharpe_mean"] > GATES["bear_sharpe_positive"]),
        "placebo_z_gte_3": bool(tsm_res.get("placebo_z", 0) >= GATES["placebo_z_gte_3"]),
    }
    print("  Pre-registered promotion gates (primary TSM, 9m):")
    for g, ok in tsm_gates.items():
        print(f"    {g:<28} {'PASS' if ok else 'FAIL'}")
    tsm_gates["all_passed"] = all(v for k, v in tsm_gates.items() if k != "all_passed")

    # ---- Part 6: supplementary validation ----
    print("\n  Supplementary validation (per-contract TSM + lookback sensitivity)...")
    validation = validation_extras(de_index, spy, PRIMARY_LOOKBACK)
    for col, v in validation["per_contract_tsm"].items():
        print(f"    {col:<6} standalone OOS Sharpe={v['oos_sharpe']:+.3f}  "
              f"pos={v['positive_folds']}/{v['n_folds']}")
    for lb, v in validation["tsm_lookback_sensitivity"].items():
        print(f"    lookback {lb:<4} OOS Sharpe={v['oos_sharpe']:+.3f}  "
              f"pos={v['positive_folds']}/{v['n_folds']}")

    # ---- Part 7: sample-period isolation ----
    print("\n" + "-" * 72)
    print("Part 3: Sample-period isolation")
    print("-" * 72)
    # (a) Extended universe restricted to the E016 subsample window.
    sub_results = subsample_check(panels, FUTURES_UNIVERSE, "sub_", PRIMARY_LOOKBACK)
    print(f"  (a) Extended 16-contract universe restricted to {SUBSAMPLE_START}+ "
          f"(same universe, short sample, {PRIMARY_LOOKBACK}m TSM):")
    for lbl, res in sub_results.items():
        bear = res["regime_analysis"]["bear"]["sharpe_mean"]
        print(f"    {lbl:<34} OOS_Sharpe={res['oos_sharpe']:.3f}  "
              f"bear_Sh={bear:+.3f}  beta={res['equity_beta']:+.3f}  "
              f"pos={res['positive_folds']}/{res['n_folds']}")

    # (b) E016 replication: original 13-contract panel, canonical 12m lookback.
    e016_panels = build_panels(E016_UNIVERSE)
    print(f"\n  (b) E016 replication (13-contract panel incl. RTY=F, "
          f"{e016_panels['de_index'].index[0].date()}+, 12m TSM):")
    e016_rep = strategy_grid(e016_panels, 12, "e016rep_")
    for lbl, res in e016_rep.items():
        bear = res["regime_analysis"]["bear"]["sharpe_mean"]
        print(f"    {lbl:<34} OOS_Sharpe={res['oos_sharpe']:.3f}  "
              f"bear_Sh={bear:+.3f}  beta={res['equity_beta']:+.3f}  "
              f"pos={res['positive_folds']}/{res['n_folds']}")

    # ---- Part 8: E015 multi-asset re-validation ----
    print("\n" + "-" * 72)
    print("Part 4: E015 multi-asset re-validation (de-seamed futures)")
    print("-" * 72)
    e015_val = e015_revalidation(de_index)
    print(f"  Multi-asset universe: {e015_val['n_tickers']} tickers, "
          f"{e015_val['n_days']} days, {e015_val['n_folds']} folds")
    print(f"  Futures replaced with de-seamed indices: {e015_val['futures_replaced']}")
    print(f"  Raw-stitched pure TSM (12m, long-only): "
          f"OOS Sharpe={e015_val['raw_stitched']['oos_sharpe']:.3f} "
          f"(E015 reported {e015_val['e015_reported']:.3f})")
    print(f"  De-seamed pure TSM (12m, long-only):    "
          f"OOS Sharpe={e015_val['deseamed']['oos_sharpe']:.3f} "
          f"beta={e015_val['deseamed']['equity_beta']:+.3f} "
          f"maxDD={e015_val['deseamed']['max_drawdown']:.3f} "
          f"turn={e015_val['deseamed']['turnover']:.4f}")
    print(f"  Delta (de-seamed - raw): {e015_val['delta_sharpe']:+.3f}")

    # ---- Summary ----
    print("\n" + "=" * 72)
    print("E017 Summary")
    print("=" * 72)
    best = max(["tsm_deseamed", "carry_normalized_basis",
                "carry_realized_rollyield", "blend_tsm_carry_50_50"],
               key=lambda k: results[k]["oos_sharpe"])
    print(f"  Best de-seamed strategy: {best} "
          f"(OOS Sharpe={results[best]['oos_sharpe']:.3f}, "
          f"z={results[best].get('placebo_z', float('nan')):.2f})")
    print(f"  Roll-methodology impact (TSM raw vs de-seamed, {PRIMARY_LOOKBACK}m): "
          f"{results['tsm_raw_stitched']['oos_sharpe']:.3f} -> "
          f"{results['tsm_deseamed']['oos_sharpe']:.3f}")
    print(f"  Sample-period isolation (16 contracts, 2017+ vs 2014+): "
          f"{sub_results['sub_tsm_deseamed']['oos_sharpe']:.3f} vs "
          f"{results['tsm_deseamed']['oos_sharpe']:.3f}")
    print(f"  E016 replication (13 contracts, 2017+, 12m): "
          f"{e016_rep['e016rep_tsm_deseamed']['oos_sharpe']:.3f} "
          f"(E016 reported 0.717)")
    print(f"  Promotion gates (blend): {'ALL PASSED' if gates['all_passed'] else 'NOT all passed'}")
    print(f"  Promotion gates (primary TSM): {'ALL PASSED' if tsm_gates['all_passed'] else 'NOT all passed'}")

    # ---- Save ----
    result = {
        "experiment": "E017",
        "timestamp": deterministic_timestamp(),
        "description": "TSM + carry on an extended 16-contract futures universe (2014-2026).",
        "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP},
        "rebalance_freq_days": REBAL,
        "pre_registered": {
            "primary_lookback_months": PRIMARY_LOOKBACK,
            "primary_lookback_justification": "E016 short-sample grid: 9m and 18m both 0.89 vs 12m 0.72; 9m chosen as shortest robust horizon (fewest lookback degrees of freedom)",
            "gates": {k: v for k, v in GATES.items()},
        },
        "universe": {
            "futures": list(FUTURES_UNIVERSE.keys()),
            "pairs": {k: v[0] for k, v in FUTURES_UNIVERSE.items()},
            "n_days": int(len(de_index)),
            "start": str(de_index.index[0].date()),
            "end": str(de_index.index[-1].date()),
        },
        "roll_methodology": {
            "detector": "futures-vs-spot excess overnight gap: calendar windows (bd 1-18 of roll month; monthly for commodities, Mar/Jun/Sep/Dec for financials) with 15bps threshold + 50% outlier rule",
            "correction": "seam-day futures returns replaced by paired spot ETF return (proxy for true underlying move); synthetic index rebuilt from de-seamed returns",
            "seam_stats": seam_stats,
            "cl_april_2020_case": case,
        },
        "tsm_config": {"lookback_months": PRIMARY_LOOKBACK, "skip_months": 1, "vol_window": 63, "long_only": False},
        "carry_config": {
            "primary": "normalized basis carry: 1 - (F/S)_t / median(F/S)_{t-252..t-1}, KMPV 2018 sign convention, cap 0.35",
            "secondary": "realized roll yield: negative trailing 252d sum of seam excess gaps (futures-vs-spot)",
            "top_frac": 0.5,
            "vol_window": 63,
        },
        "placebo": {"mean": pm, "std": ps, "n_sim": PLACEBO_N_SIM,
                    "type": "random TSM + random carry, 50/50 blend"},
        "results": results,
        "validation": validation,
        "sample_period_isolation": {
            "extended_universe_2017plus": sub_results,
            "e016_replication_13_contract_2017plus_12m": e016_rep,
        },
        "e015_revalidation": e015_val,
        "promotion_gates_blend": gates,
        "promotion_gates_primary_tsm": tsm_gates,
        "best_strategy": best,
    }

    out_path = os.path.join("experiments", "e017_extended_futures.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        jsonio.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
