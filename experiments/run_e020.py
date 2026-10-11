#!/usr/bin/env python3
"""E020: Robustness validation of the promoted E019 total portfolio.

Follows the E019 handoff. E019 promoted a total portfolio (equity
flagship TSM 12m long-only inv-vol large_liquid + de-seamed futures
sleeve TSM-18m) at futures weights 0.25 (OOS 2.175) and 0.50 (2.034),
both clearing the pre-registered gates. E020 is a pre-registered
robustness battery, all gates set before running, on the same
common-calendar 3205-day / 42-fold panel.

Part A - execution-convention alignment.
Part B - cost sweep on the promoted portfolios.
Part C - equity lookback sensitivity.
Part D - futures-sleeve variant (Part-A blend vs pure TSM-18m).
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src import data, backtest, strategies, futures
from src.run_experiment import UNIVERSES
from run_e017 import (
    build_panels, evaluate, walk_forward, regime_summary,
    market_diagnostics, compute_drawdown, blended_placebo,
    FUTURES_UNIVERSE, TC_COST, SLIPPAGE, TRAIN, TEST, STEP, REBAL,
    SEED, PLACEBO_N_SIM, START,
)
from run_e018 import permuted_roll_yield, permuted_carry_panel

# ---------------------------------------------------------------------------
# Pre-registered design (fixed before running; see module docstring).
# ---------------------------------------------------------------------------

# Promoted E019 total portfolios (gate references, common calendar).
PROMOTED = {
    "futures_weight_0.25": {"oos_sharpe": 2.175, "bear_sharpe": -0.516,
                            "max_dd": -0.243, "turnover": 0.0602,
                            "equity_beta": -0.051},
    "futures_weight_0.50": {"oos_sharpe": 2.034, "bear_sharpe": 0.059,
                            "max_dd": -0.176, "turnover": 0.0563,
                            "equity_beta": -0.037},
}
EQUITY_FLAGSHIP_COMMON = {"oos_sharpe": 2.157, "bear_sharpe": -0.816,
                           "max_dd": -0.313, "turnover": 0.0640,
                           "equity_beta": -0.065}

# Part A: execution-convention alignment.
# Gate: the convention-aligned total portfolio must keep OOS Sharpe >= 2.0
# AND bear Sharpe strictly greater than the convention-aligned equity-only
# baseline (both on the same aligned calendar/convention).
ALIGN_GATES = {"oos_sharpe_gte_2.0": 2.0,
               "bear_sharpe_gt_aligned_equity": None}

# Part B: cost sweep on the promoted portfolios.
COST_SCENARIOS = {
    "base_0.5_0.2bps": (0.0005, 0.0002),
    "high_20_5bps": (0.0020, 0.0005),
    "zero_cost": (0.0, 0.0),
}
# Gate: promoted portfolios keep OOS Sharpe >= 2.0 at the high-cost scenario.
COST_GATES = {"high_cost_oos_sharpe_gte_2.0": 2.0}

# Part C: equity lookback sensitivity {9, 12, 18}m (12m registered primary).
EQUITY_LOOKBACKS = [9, 12, 18]
# Gate: the 12m construction remains the best or near-best; a lookback that
# collapses the total portfolio below 2.0 signals fragility. No gate on the
# grid itself (multiple-testing awareness); the promoted weight is fixed at
# 0.25 and only the equity sleeve lookback varies.
LOOKBACK_GATES = {"total_oos_sharpe_gte_2.0": 2.0}

# Part D: futures-sleeve variant at the promoted 25% futures weight.
# Gate: the Part-A-promoted blend sleeve (TSM weight 0.5, E019) must beat
# pure TSM-18m at the same 25% futures weight (pre-registered falsification).
D_FUTURES_WEIGHT = 0.25
D_TSM_LOOKBACK = 18
D_CARRY_WINDOW = 252
D_BLEND_TSM_WEIGHTS = [0.5, 0.7]
D_GATES = {"blend_beats_pure_tsm18m": True}

# E019 recorded anchors (replication checks, deterministic).
E019_ANCHORS = {
    "equity_flagship_common": EQUITY_FLAGSHIP_COMMON,
    "total_0.25": PROMOTED["futures_weight_0.25"],
    "total_0.50": PROMOTED["futures_weight_0.50"],
}


def _fold_metrics_to_sharpes(fm):
    return [m["sharpe"] for m in fm
            if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]


def eval_net_series(net, spy_ret, index_df, turnover, label):
    """Walk-forward + diagnostics for a net-return series on a calendar."""
    rets = pd.DataFrame({"gross": net, "costs": pd.Series(0.0, index=net.index),
                         "net": net})
    diag = market_diagnostics(rets, spy_ret)
    fm, splits = walk_forward(rets, index_df, spy_ret)
    s = _fold_metrics_to_sharpes(fm)
    oos_sharpe = float(np.mean(s)) if s else float("nan")
    oos_std = float(np.std(s)) if s else float("nan")
    dd, uw = compute_drawdown(rets["net"])
    reg = regime_summary(fm)
    n_pos = int(sum(1 for m in fm if m.get("sharpe") is not None and m.get("sharpe", 0) > 0))
    return {
        "label": label,
        "oos_sharpe": oos_sharpe,
        "oos_sharpe_std": oos_std,
        "turnover": turnover,
        "equity_beta": diag["equity_beta"],
        "corr_spy": diag["corr_spy"],
        "alpha_annual": diag["alpha_annual"],
        "max_drawdown": dd,
        "time_underwater_days": uw,
        "positive_folds": n_pos,
        "n_folds": len(splits),
        "regime_analysis": reg,
    }


def equity_flagship(close, open_, lookback=12):
    """E010/E015 equity flagship: pure TSM, long-only, inv-vol (63d)."""
    sig = strategies.time_series_momentum_pure(close, lookback=lookback, skip=1)
    w = backtest.time_series_momentum_weights(sig, close, long_only=True, vol_window=63)
    return w


def futures_sleeve(de_index, lookback=18):
    """Futures sleeve: symmetric TSM on de-seamed indices."""
    sig = strategies.time_series_momentum_pure(de_index, lookback=lookback, skip=1)
    w = backtest.time_series_momentum_weights(sig, de_index, long_only=False, vol_window=63)
    return w


# ---------------------------------------------------------------------------
# Part A: execution-convention alignment.
# ---------------------------------------------------------------------------

def aligned_equity_returns(close_c, open_c, w_eq, tc, sl, rebal):
    """Equity sleeve returns under a chosen execution convention.

    close_to_close: de-seamed-style close-to-close (no observable next open
    on the common calendar); matches the futures sleeve convention.
    next_open: the repo's standard next-day-open equity convention.
    """
    out = {}
    w = backtest.shift_weights(w_eq)
    if rebal > 1:
        w = backtest._rebalance_weights(w, rebal)
    asset_cc = close_c.pct_change()
    gross_cc = (w * asset_cc).sum(axis=1)
    turnover_cc = (w.diff().abs()).sum(axis=1)
    out["close_to_close"] = pd.DataFrame({
        "gross": gross_cc,
        "costs": turnover_cc * (tc + sl),
        "net": gross_cc - turnover_cc * (tc + sl),
    })
    asset_no = (open_c.shift(-1) / close_c - 1.0)
    gross_no = (w * asset_no).sum(axis=1)
    turnover_no = (w.diff().abs()).sum(axis=1)
    out["next_open"] = pd.DataFrame({
        "gross": gross_no,
        "costs": turnover_no * (tc + sl),
        "net": gross_no - turnover_no * (tc + sl),
    })
    return out


def part_a(close_c, open_c, de_index, spy, common, w_eq, w_fut):
    """Execution-convention alignment test.

    Builds the total portfolio under (a) the repo's mixed convention
    (equity next-open, futures close-to-close) and (b) a convention-
    aligned construction where BOTH sleeves earn close-to-close on the
    common calendar. Gates reference the aligned equity-only baseline.
    """
    spy_ret = spy.pct_change().fillna(0.0)
    index_df = pd.DataFrame(index=common)
    eq_turn = backtest.average_turnover(w_eq)
    fut_turn = backtest.average_turnover(w_fut)

    # Futures sleeve (close-to-close by construction).
    fut_ret = backtest.portfolio_returns_rebalance_clean(
        w_fut, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE,
        rebalance_freq=REBAL
    )

    results = {}
    for conv in ["next_open", "close_to_close"]:
        eq_ret = aligned_equity_returns(close_c, open_c, w_eq,
                                        TC_COST, SLIPPAGE, REBAL)[conv]
        eq_ret = eq_ret.reindex(common)
        fut_ret_c = fut_ret.reindex(common)
        eq_bear = None
        for w_f in [0.25, 0.50]:
            tot = (1.0 - w_f) * eq_ret["net"] + w_f * fut_ret_c["net"]
            tot_turn = (1.0 - w_f) * eq_turn + w_f * fut_turn
            res = eval_net_series(tot, spy_ret, index_df, tot_turn,
                                  f"total_{conv}_fut{w_f:.2f}")
            results[f"{conv}_fut{w_f:.2f}"] = res
        # Aligned equity-only baseline (same convention).
        eq_res = eval_net_series(eq_ret["net"], spy_ret, index_df,
                                 eq_turn, f"equity_only_{conv}")
        results[f"equity_only_{conv}"] = eq_res
        eq_bear = eq_res["regime_analysis"]["bear"]["sharpe_mean"]
        for w_f in [0.25, 0.50]:
            res = results[f"{conv}_fut{w_f:.2f}"]
            res["gates"] = {
                "oos_sharpe_gte_2.0": bool(
                    res["oos_sharpe"] >= ALIGN_GATES["oos_sharpe_gte_2.0"]),
                "bear_sharpe_gt_aligned_equity": bool(
                    res["regime_analysis"]["bear"]["sharpe_mean"] > eq_bear),
            }
            res["gates"]["all_passed"] = all(
                v for k, v in res["gates"].items() if k != "all_passed")
    return results


def part_a_summary(results):
    print("\n" + "=" * 72)
    print("Part A: Execution-convention alignment")
    print("=" * 72)
    for k in ["equity_only_next_open", "equity_only_close_to_close",
              "next_open_fut0.25", "next_open_fut0.50",
              "close_to_close_fut0.25", "close_to_close_fut0.50"]:
        r = results[k]
        bear = r["regime_analysis"]["bear"]["sharpe_mean"]
        print(f"  {k:<32} OOS={r['oos_sharpe']:.3f}  "
              f"beta={r['equity_beta']:+.3f}  bear={bear:+.3f}  "
              f"maxDD={r['max_drawdown']:.3f}  turn={r['turnover']:.4f}  "
              f"pos={r['positive_folds']}/{r['n_folds']}")
    print("  Gates (aligned construction):")
    for w_f in [0.25, 0.50]:
        r = results[f"close_to_close_fut{w_f:.2f}"]
        print(f"    fut_w={w_f:.2f}  "
              f"{'PASS' if r['gates']['all_passed'] else 'FAIL'}  "
              f"(OOS>=2.0: {'PASS' if r['gates']['oos_sharpe_gte_2.0'] else 'FAIL'}, "
              f"bear>aligned equity: "
              f"{'PASS' if r['gates']['bear_sharpe_gt_aligned_equity'] else 'FAIL'})")


# ---------------------------------------------------------------------------
# Part B: cost sweep on the promoted portfolios.
# ---------------------------------------------------------------------------

def part_b(close_c, open_c, de_index, spy, common, w_eq, w_fut):
    """Cost sweep {base, 20bps+5bps, zero} on the promoted 25%/50% portfolios."""
    spy_ret = spy.pct_change().fillna(0.0)
    index_df = pd.DataFrame(index=common)
    eq_turn = backtest.average_turnover(w_eq)
    fut_turn = backtest.average_turnover(w_fut)
    w = backtest.shift_weights(w_eq)
    w_f = backtest.shift_weights(w_fut)
    if REBAL > 1:
        w = backtest._rebalance_weights(w, REBAL)
        w_f = backtest._rebalance_weights(w_f, REBAL)
    asset_no = (open_c.shift(-1) / close_c - 1.0)
    asset_cc = close_c.pct_change()
    asset_fut = de_index.pct_change()

    results = {}
    for name, (tc, sl) in COST_SCENARIOS.items():
        eq_gross = (w * asset_no).sum(axis=1)
        eq_turn_t = (w.diff().abs()).sum(axis=1)
        eq_net = eq_gross - eq_turn_t * (tc + sl)
        fut_gross = (w_f * asset_fut).sum(axis=1)
        fut_turn_t = (w_f.diff().abs()).sum(axis=1)
        fut_net = fut_gross - fut_turn_t * (tc + sl)
        row = {"cost_scenario": name, "tc_cost": tc, "slippage": sl}
        for w_f in [0.25, 0.50]:
            tot = (1.0 - w_f) * eq_net + w_f * fut_net
            tot_turn = (1.0 - w_f) * eq_turn + w_f * fut_turn
            res = eval_net_series(tot, spy_ret, index_df, tot_turn,
                                  f"total_fut{w_f:.2f}_{name}")
            res["gates"] = {
                "high_cost_oos_sharpe_gte_2.0": bool(
                    res["oos_sharpe"] >= COST_GATES["high_cost_oos_sharpe_gte_2.0"]
                    if name == "high_20_5bps" else True),
            }
            res["gates"]["all_passed"] = all(
                v for k, v in res["gates"].items() if k != "all_passed")
            row[f"fut{w_f:.2f}"] = res
        results[name] = row
    return results


def part_b_summary(results):
    print("\n" + "=" * 72)
    print("Part B: Cost sweep on the promoted portfolios")
    print("=" * 72)
    header = (f"  {'scenario':<20} {'fut_w':<8} {'OOS':>7} {'beta':>7} "
              f"{'bear':>7} {'maxDD':>7} {'turn':>7} {'pos':>7}  gate")
    print(header)
    for name, row in results.items():
        for w_f in [0.25, 0.50]:
            r = row[f"fut{w_f:.2f}"]
            bear = r["regime_analysis"]["bear"]["sharpe_mean"]
            print(f"  {name:<20} {w_f:<8} {r['oos_sharpe']:>7.3f} "
                  f"{r['equity_beta']:>7.3f} {bear:>7.3f} "
                  f"{r['max_drawdown']:>7.3f} {r['turnover']:>7.4f} "
                  f"{r['positive_folds']:>3}/{r['n_folds']:<3}  "
                  f"{'PASS' if r['gates']['all_passed'] else 'n/a'}")


# ---------------------------------------------------------------------------
# Part C: equity lookback sensitivity {9,12/18}m (12m registered primary).
# ---------------------------------------------------------------------------

def part_c(close_c, open_c, de_index, spy, common, w_fut):
    """Vary the equity sleeve lookback at the promoted 25% futures weight."""
    spy_ret = spy.pct_change().fillna(0.0)
    index_df = pd.DataFrame(index=common)
    fut_ret = backtest.portfolio_returns_rebalance_clean(
        w_fut, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE,
        rebalance_freq=REBAL
    ).reindex(common)
    fut_turn = backtest.average_turnover(w_fut)

    results = {}
    for lb in EQUITY_LOOKBACKS:
        w_eq = equity_flagship(close_c, open_c, lookback=lb)
        eq_turn = backtest.average_turnover(w_eq)
        eq_ret = backtest.portfolio_returns_rebalance_clean(
            w_eq, close_c, open_c, tc_cost=TC_COST, slippage=SLIPPAGE,
            rebalance_freq=REBAL
        ).reindex(common)
        eq_res = eval_net_series(eq_ret["net"], spy_ret, index_df, eq_turn,
                                 f"equity_only_{lb}m")
        tot = (1.0 - D_FUTURES_WEIGHT) * eq_ret["net"] + \
            D_FUTURES_WEIGHT * fut_ret["net"]
        tot_turn = (1.0 - D_FUTURES_WEIGHT) * eq_turn + \
            D_FUTURES_WEIGHT * fut_turn
        t_res = eval_net_series(tot, spy_ret, index_df, tot_turn,
                                f"total_{lb}m_fut{D_FUTURES_WEIGHT:.2f}")
        t_res["gates"] = {
            "total_oos_sharpe_gte_2.0": bool(
                t_res["oos_sharpe"] >= LOOKBACK_GATES["total_oos_sharpe_gte_2.0"]),
        }
        t_res["gates"]["all_passed"] = all(
            v for k, v in t_res["gates"].items() if k != "all_passed")
        results[f"{lb}m"] = {"equity_only": eq_res, "total": t_res}
    return results


def part_c_summary(results):
    print("\n" + "=" * 72)
    print("Part C: Equity lookback sensitivity (futures weight 0.25)")
    print("=" * 72)
    for lb, v in results.items():
        e = v["equity_only"]
        t = v["total"]
        print(f"  lookback={lb:<3} equity OOS={e['oos_sharpe']:.3f}  "
              f"bear={e['regime_analysis']['bear']['sharpe_mean']:+.3f}  "
              f"maxDD={e['max_drawdown']:.3f}  turn={e['turnover']:.4f}  "
              f"pos={e['positive_folds']}/{e['n_folds']}")
        print(f"         total  OOS={t['oos_sharpe']:.3f}  "
              f"bear={t['regime_analysis']['bear']['sharpe_mean']:+.3f}  "
              f"maxDD={t['max_drawdown']:.3f}  turn={t['turnover']:.4f}  "
              f"pos={t['positive_folds']}/{t['n_folds']}  "
              f"gates={'PASS' if t['gates']['all_passed'] else 'FAIL'}")


# ---------------------------------------------------------------------------
# Part D: futures-sleeve variant (Part-A blend vs pure TSM-18m).
# ---------------------------------------------------------------------------

def part_d(de_index, spy, common, carry_rroll, seams_dt):
    """Futures-sleeve variant at the promoted 25% futures weight.

    Pre-registered falsification: the Part-A-promoted blend sleeve
    (TSM-18m weight 0.5, E019) must beat pure TSM-18m at the same 25%
    total futures weight.
    """
    spy_ret = spy.pct_change().fillna(0.0)
    index_df = pd.DataFrame(index=common)
    vol = de_index.pct_change().rolling(63).std().replace(0, np.nan)
    w_tsm18 = futures_sleeve(de_index, lookback=D_TSM_LOOKBACK)
    w_carry = backtest.carry_weights(carry_rroll, vol)

    sleeves = {"pure_tsm18m": w_tsm18}
    for tsm_w in D_BLEND_TSM_WEIGHTS:
        sleeves[f"blend_tsm{tsm_w:.1f}"] = tsm_w * w_tsm18 + \
            (1.0 - tsm_w) * w_carry

    results = {}
    for name, w in sleeves.items():
        turn = backtest.average_turnover(w)
        ret = backtest.portfolio_returns_rebalance_clean(
            w, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE,
            rebalance_freq=REBAL
        ).reindex(common)
        res = eval_net_series(ret["net"], spy_ret, index_df, turn,
                              f"futures_sleeve_{name}")
        results[name] = res

    pure = results["pure_tsm18m"]
    for name in [f"blend_tsm{tsm_w:.1f}" for tsm_w in D_BLEND_TSM_WEIGHTS]:
        r = results[name]
        r["beats_pure_tsm18m"] = bool(r["oos_sharpe"] > pure["oos_sharpe"])
        r["gates"] = {"blend_beats_pure_tsm18m": r["beats_pure_tsm18m"]}
        r["gates"]["all_passed"] = r["beats_pure_tsm18m"]
    return results


def part_d_summary(results):
    print("\n" + "=" * 72)
    print("Part D: Futures-sleeve variant (pure TSM-18m vs Part-A blend)")
    print("=" * 72)
    for name, r in results.items():
        bear = r["regime_analysis"]["bear"]["sharpe_mean"]
        print(f"  {name:<24} OOS={r['oos_sharpe']:.3f}  "
              f"beta={r['equity_beta']:+.3f}  bear={bear:+.3f}  "
              f"maxDD={r['max_drawdown']:.3f}  turn={r['turnover']:.4f}  "
              f"pos={r['positive_folds']}/{r['n_folds']}  "
              f"beats_pure={r.get('beats_pure_tsm18m', False)}")
    }")# ---- Save ----
