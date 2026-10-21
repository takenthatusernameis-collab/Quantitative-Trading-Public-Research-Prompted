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
Part E - fine futures-weight grid (sensitivity only).

PRE-REGISTERED BEFORE RUNNING (gates set ex-ante, goalposts not
movable after the run; see the E019 handoff for the authoritative
specification):

  Part A - execution-convention alignment. Re-run the total
    portfolio with the equity sleeve on close-to-close returns
    (matching the futures convention). Gate: the 25% portfolio
    must keep OOS Sharpe >= 2.0 AND bear Sharpe strictly greater
    than the convention-aligned equity-only baseline (both on the
    same aligned convention/calendar). If it fails, the promotion
    is convention-dependent - demote and record the negative.

  Part B - cost sweep on the promoted portfolios (25% and 50%):
    base (0.5+0.2bps), high (20+5bps), zero. No promotion gate
    (measurement); record whether the 2.0 gate survives high costs.

  Part C - equity lookback sensitivity {9, 12, 18}m at the
    promoted 25% futures weight; 12m is the registered primary.
    Sensitivity only (multiple-testing awareness): a lookback that
    collapses the total portfolio below 2.0 signals fragility.

  Part D - futures-sleeve variant at the promoted 25% futures
    weight: pure TSM-18m (E019 pre-registered primary) vs the
    Part-A-promoted blend sleeve (TSM weight 0.5/0.7). Pre-
    registered falsification: the blend sleeve must beat pure
    TSM-18m on TOTAL-portfolio OOS Sharpe to replace it.

  Part E - fine futures-weight grid {0.10, 0.15, 0.20, 0.30,
    0.40, 0.60} at the primary configuration. Sensitivity only
    (the 0.25/0.50 cells are E019's pre-registered cells).

Replication anchors (E019, deterministic): equity flagship
(common calendar) OOS 2.157 / bear -0.816 / maxDD -0.313 /
turnover 0.0640 / beta -0.065; total 0.25 OOS 2.175; total 0.50
OOS 2.034; TSM-18m sleeve OOS 0.805. The next_open convention
must reproduce E019 exactly - this is the integrity check for the
whole battery.

Premise verification (prioritization v1.2.1 mandatory step): every
factual premise in the E019 handoff was verified against
experiments/e019_cross_asset_portfolio.json before pre-registration
(promoted weights, metrics, turnover, anchors - all match to <5e-4).
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
from src import jsonio
from src.run_experiment import UNIVERSES, deterministic_timestamp
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

EQUITY_TSM_LOOKBACK = 12   # E010/E015 flagship construction (registered primary)

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

# E019 recorded anchors (full precision, from e019_cross_asset_portfolio.json)
# for the replication check under the next_open convention.
E019_ANCHOR_VALUES = {
    "equity_only_next_open": 2.1568422990612084,
    "next_open_fut0.25": 2.1750081709472355,
    "next_open_fut0.50": 2.034365907971341,
}
E019_ANCHOR_TOL = 5e-4

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
# Measurement (not a promotion gate, per the E019 handoff): record
# whether the 2.0 gate survives the high-cost scenario.
COST_MEASUREMENT_BAR = {"high_cost_oos_sharpe_gte_2.0": 2.0}

# Part C: equity lookback sensitivity {9, 12, 18}m (12m registered primary).
EQUITY_LOOKBACKS = [9, 12, 18]
# Sensitivity only (multiple-testing awareness): the 12m construction is
# the registered primary; a lookback that collapses the total portfolio
# below 2.0 signals fragility.
LOOKBACK_MEASUREMENT_BAR = {"total_oos_sharpe_gte_2.0": 2.0}

# Part D: futures-sleeve variant at the promoted 25% futures weight.
# Gate: the Part-A-promoted blend sleeve (TSM weight 0.5/0.7, E019) must
# beat pure TSM-18m at the same 25% total futures weight on TOTAL-portfolio
# OOS Sharpe (pre-registered falsification).
D_FUTURES_WEIGHT = 0.25
D_TSM_LOOKBACK = 18
D_CARRY_WINDOW = 252
D_BLEND_TSM_WEIGHTS = [0.5, 0.7]
D_GATES = {"blend_beats_pure_tsm18m": True}

# Part E: fine futures-weight grid at the primary configuration
# (sensitivity only; 0.25/0.50 are E019's pre-registered cells).
FINE_GRID = [0.10, 0.15, 0.20, 0.30, 0.40, 0.60]


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


def equity_flagship(close, open_, lookback=EQUITY_TSM_LOOKBACK):
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
    # Forward close-to-close (t -> t+1), matching the futures
    # sleeve convention (portfolio_returns_rebalance_clean with
    # open_ = close). Using pct_change() here would credit the
    # backward (t-1 -> t) return - a one-day timing mismatch
    # with the futures sleeve.
    asset_cc = close_c.shift(-1) / close_c - 1.0
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
    """Cost sweep {base, 20bps+5bps, zero} on the promoted 25%/50% portfolios.

    Uses the repo's standard construction per sleeve (equity
    next-open, futures close-to-close) at each cost scenario, so
    the base scenario reproduces the E019 promoted portfolios
    exactly (built-in consistency check).
    """
    spy_ret = spy.pct_change().fillna(0.0)
    index_df = pd.DataFrame(index=common)
    eq_turn = backtest.average_turnover(w_eq)
    fut_turn = backtest.average_turnover(w_fut)

    results = {}
    for name, (tc, sl) in COST_SCENARIOS.items():
        eq_r = backtest.portfolio_returns_rebalance_clean(
            w_eq, close_c, open_c, tc_cost=tc, slippage=sl,
            rebalance_freq=REBAL)
        fut_r = backtest.portfolio_returns_rebalance_clean(
            w_fut, de_index, de_index, tc_cost=tc, slippage=sl,
            rebalance_freq=REBAL)
        row = {"cost_scenario": name, "tc_cost": tc, "slippage": sl}
        for w_f_ in [0.25, 0.50]:
            tot = (1.0 - w_f_) * eq_r["net"] + w_f_ * fut_r["net"]
            tot_turn = (1.0 - w_f_) * eq_turn + w_f_ * fut_turn
            res = eval_net_series(tot, spy_ret, index_df, tot_turn,
                                  f"total_fut{w_f_:.2f}_{name}")
            res["high_cost_gate_survives"] = bool(
                res["oos_sharpe"] >= COST_MEASUREMENT_BAR["high_cost_oos_sharpe_gte_2.0"]
            ) if name == "high_20_5bps" else None
            row[f"fut{w_f_:.2f}"] = res
        results[name] = row
    return results


def part_b_summary(results):
    print("\n" + "=" * 72)
    print("Part B: Cost sweep on the promoted portfolios")
    print("=" * 72)
    header = (f"  {'scenario':<20} {'fut_w':<8} {'OOS':>7} {'beta':>7} "
              f"{'bear':>7} {'maxDD':>7} {'turn':>7} {'pos':>7}  2.0@high")
    print(header)
    for name, row in results.items():
        for w_f in [0.25, 0.50]:
            r = row[f"fut{w_f:.2f}"]
            bear = r["regime_analysis"]["bear"]["sharpe_mean"]
            gate = ("n/a" if r["high_cost_gate_survives"] is None
                    else ("survives" if r["high_cost_gate_survives"] else "BREACHED"))
            print(f"  {name:<20} {w_f:<8} {r['oos_sharpe']:>7.3f} "
                  f"{r['equity_beta']:>7.3f} {bear:>7.3f} "
                  f"{r['max_drawdown']:>7.3f} {r['turnover']:>7.4f} "
                  f"{r['positive_folds']:>3}/{r['n_folds']:<3}  {gate}")


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
        t_res["bar_check"] = {
            "total_oos_sharpe_gte_2.0": bool(
                t_res["oos_sharpe"] >= LOOKBACK_MEASUREMENT_BAR["total_oos_sharpe_gte_2.0"]),
        }
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
              f"OOS>=2.0: {'YES' if t['bar_check']['total_oos_sharpe_gte_2.0'] else 'NO'}")


# ---------------------------------------------------------------------------
# Part D: futures-sleeve variant (Part-A blend vs pure TSM-18m).
# ---------------------------------------------------------------------------

def part_d(eq_close, eq_open, de_index, spy, common, carry_rroll):
    """Futures-sleeve variant at the promoted 25% futures weight.

    Pre-registered falsification: the Part-A-promoted blend sleeve
    (TSM weight 0.5/0.7, E019) must beat pure TSM-18m at the same
    25% total futures weight on TOTAL-portfolio OOS Sharpe.
    """
    spy_ret = spy.pct_change().fillna(0.0)
    index_df = pd.DataFrame(index=common)
    vol = de_index.pct_change().rolling(63).std().replace(0, np.nan)
    w_tsm18 = futures_sleeve(de_index, lookback=D_TSM_LOOKBACK)
    w_carry = backtest.carry_weights(carry_rroll, vol)

    # Equity sleeve (fixed, E019 construction, next-open execution).
    w_eq = equity_flagship(eq_close, eq_open, lookback=EQUITY_TSM_LOOKBACK)
    eq_ret = backtest.portfolio_returns_rebalance_clean(
        w_eq, eq_close, eq_open, tc_cost=TC_COST, slippage=SLIPPAGE,
        rebalance_freq=REBAL
    )
    eq_turn = backtest.average_turnover(w_eq)

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
        # Sleeve standalone (context).
        sleeve_res = eval_net_series(ret["net"], spy_ret, index_df, turn,
                                     f"futures_sleeve_{name}")
        # Total portfolio at the promoted 25% futures weight (the
        # pre-registered comparison).
        tot = (1.0 - D_FUTURES_WEIGHT) * eq_ret["net"] + \
            D_FUTURES_WEIGHT * ret["net"]
        tot_turn = (1.0 - D_FUTURES_WEIGHT) * eq_turn + \
            D_FUTURES_WEIGHT * turn
        tot_res = eval_net_series(tot, spy_ret, index_df, tot_turn,
                                  f"total_fut{D_FUTURES_WEIGHT:.2f}_sleeve_{name}")
        results[name] = {"sleeve_standalone": sleeve_res, "total": tot_res}

    pure = results["pure_tsm18m"]["total"]
    for name in [f"blend_tsm{tsm_w:.1f}" for tsm_w in D_BLEND_TSM_WEIGHTS]:
        r = results[name]
        r["beats_pure_tsm18m"] = bool(
            r["total"]["oos_sharpe"] > pure["oos_sharpe"])
        r["gates"] = {"blend_beats_pure_tsm18m": r["beats_pure_tsm18m"]}
        r["gates"]["all_passed"] = r["beats_pure_tsm18m"]
    return results


def part_d_summary(results):
    print("\n" + "=" * 72)
    print("Part D: Futures-sleeve variant (pure TSM-18m vs Part-A blend)")
    print("=" * 72)
    print("  (gate on TOTAL-portfolio OOS Sharpe at futures weight "
          f"{D_FUTURES_WEIGHT:.2f})")
    for name, r in results.items():
        s = r["sleeve_standalone"]
        t = r["total"]
        print(f"  {name:<24} sleeve OOS={s['oos_sharpe']:.3f}  "
              f"total OOS={t['oos_sharpe']:.3f}  "
              f"beta={t['equity_beta']:+.3f}  "
              f"bear={t['regime_analysis']['bear']['sharpe_mean']:+.3f}  "
              f"maxDD={t['max_drawdown']:.3f}  turn={t['turnover']:.4f}  "
              f"pos={t['positive_folds']}/{t['n_folds']}  "
              f"beats_pure={r.get('beats_pure_tsm18m', False)}")


# ---------------------------------------------------------------------------
# Part E: fine futures-weight grid (sensitivity only).
# ---------------------------------------------------------------------------

def part_e(eq_close, eq_open, de_index, spy, common, w_fut):
    """Fine futures-weight grid at the primary configuration.

    Sensitivity only: the 0.25/0.50 cells are E019's pre-registered
    cells; this grid maps the neighborhood with multiple-testing
    awareness (no selection).
    """
    spy_ret = spy.pct_change().fillna(0.0)
    index_df = pd.DataFrame(index=common)
    w_eq = equity_flagship(eq_close, eq_open, lookback=EQUITY_TSM_LOOKBACK)
    eq_ret = backtest.portfolio_returns_rebalance_clean(
        w_eq, eq_close, eq_open, tc_cost=TC_COST, slippage=SLIPPAGE,
        rebalance_freq=REBAL
    )
    eq_turn = backtest.average_turnover(w_eq)
    fut_ret = backtest.portfolio_returns_rebalance_clean(
        w_fut, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE,
        rebalance_freq=REBAL
    ).reindex(common)
    fut_turn = backtest.average_turnover(w_fut)

    results = {}
    for w_f in FINE_GRID:
        tot = (1.0 - w_f) * eq_ret["net"] + w_f * fut_ret["net"]
        tot_turn = (1.0 - w_f) * eq_turn + w_f * fut_turn
        res = eval_net_series(tot, spy_ret, index_df, tot_turn,
                              f"total_fut{w_f:.2f}")
        res["futures_weight"] = w_f
        results[f"futures_weight_{w_f:.2f}"] = res
    return results


def part_e_summary(results):
    print("\n" + "=" * 72)
    print("Part E: Fine futures-weight grid (sensitivity only)")
    print("=" * 72)
    for k, r in results.items():
        print(f"  {k:<24} OOS={r['oos_sharpe']:.3f}  "
              f"beta={r['equity_beta']:+.3f}  "
              f"bear={r['regime_analysis']['bear']['sharpe_mean']:+.3f}  "
              f"maxDD={r['max_drawdown']:.3f}  turn={r['turnover']:.4f}  "
              f"pos={r['positive_folds']}/{r['n_folds']}")


# ---------------------------------------------------------------------------
# Main.
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-sim", type=int, default=PLACEBO_N_SIM,
                        help="placebo simulations (unused in E020; kept for CLI parity)")
    args = parser.parse_args()

    print("=" * 72)
    print("E020: Robustness Validation of the Promoted E019 Total Portfolio")
    print("=" * 72)
    print("Pre-registered battery (gates set before running):")
    print("  Part A: convention-aligned (close-to-close equity) total portfolio")
    print("          keeps OOS Sharpe >= 2.0 AND bear Sharpe > the aligned")
    print("          equity-only baseline")
    print("  Part B: cost sweep {base, 20+5bps, zero} on the promoted 25%/50%")
    print("          portfolios (measurement: does the 2.0 gate survive high cost?)")
    print("  Part C: equity lookback sensitivity {9,12,18}m at w=0.25 (12m primary)")
    print("  Part D: blend sleeve (TSM w 0.5/0.7) vs pure TSM-18m at w=0.25;")
    print("          falsification: blend sleeve must beat pure on TOTAL OOS Sharpe")
    print("  Part E: fine futures-weight grid (sensitivity only)")

    # ---- Panels and common calendar ----
    panels = build_panels(FUTURES_UNIVERSE)
    de_index = panels["de_index"]
    carry_rroll = panels["carry_rroll"]
    spy = panels["spy"]

    eq_df = data.download(UNIVERSES["large_liquid"], start=START)
    eq_close_full = data.get_panel(eq_df, "Close").dropna(axis=1, how="all").dropna(how="all")
    eq_open_full = data.get_panel(eq_df, "Open").reindex(eq_close_full.index).fillna(eq_close_full)

    common = de_index.index
    eq_close = eq_close_full.reindex(common)
    eq_open = eq_open_full.reindex(common)
    spy_ret = spy.pct_change().fillna(0.0)
    index_df = pd.DataFrame(index=common)

    print(f"\nFutures panel: {len(de_index)} days, {de_index.shape[1]} contracts "
          f"({common[0].date()} to {common[-1].date()})")
    print(f"Equity panel (large_liquid): {len(eq_close_full)} days, "
          f"{eq_close_full.shape[1]} tickers on its own calendar")
    print(f"Common calendar: {len(common)} days "
          f"({len(eq_close_full) - len(common)} equity-only days dropped)")
    print(f"Equity tickers present: {eq_close.shape[1]} "
          f"(missing from yfinance: "
          f"{[t for t in UNIVERSES['large_liquid'] if t not in eq_close_full.columns]})")

    # ---- Part 0: E019 replication anchors (next_open convention) ----
    w_eq = equity_flagship(eq_close, eq_open)
    w_fut = futures_sleeve(de_index, lookback=18)
    eq_ret = backtest.portfolio_returns_rebalance_clean(
        w_eq, eq_close, eq_open, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
    )
    eq_turn = backtest.average_turnover(w_eq)
    fut_ret = backtest.portfolio_returns_rebalance_clean(
        w_fut, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
    )
    fut_turn = backtest.average_turnover(w_fut)
    eq_res = eval_net_series(eq_ret["net"], spy_ret, index_df, eq_turn,
                             "equity_flagship_tsm12m")
    replication = {"equity_only_next_open": eq_res}
    for w_f in [0.25, 0.50]:
        tot = (1.0 - w_f) * eq_ret["net"] + w_f * fut_ret["net"]
        tot_turn = (1.0 - w_f) * eq_turn + w_f * fut_turn
        res = eval_net_series(tot, spy_ret, index_df, tot_turn, f"total_fut{w_f:.2f}")
        replication[f"next_open_fut{w_f:.2f}"] = res
    print("\n" + "-" * 72)
    print("Part 0: E019 replication anchors (next_open convention)")
    print("-" * 72)
    all_replicated = True
    for key, anchor in E019_ANCHOR_VALUES.items():
        computed = replication[key]["oos_sharpe"]
        delta = computed - anchor
        ok = abs(delta) < E019_ANCHOR_TOL
        all_replicated = all_replicated and ok
        print(f"  {key:<26} OOS={computed:.6f}  E019={anchor:.6f}  "
              f"delta={delta:+.6f}  {'REPLICATED' if ok else 'DIFFERS'}")
    print(f"  Inter-sleeve daily net-return correlation: "
          f"{float(eq_ret['net'].corr(fut_ret['net'])):+.3f}")
    if not all_replicated:
        print("  WARNING: E019 anchors did NOT replicate - the battery's "
              "equity-sleeve construction differs from E019's.")

    # ---- Part A ----
    a_results = part_a(eq_close, eq_open, de_index, spy, common, w_eq, w_fut)
    part_a_summary(a_results)

    # ---- Part B ----
    b_results = part_b(eq_close, eq_open, de_index, spy, common, w_eq, w_fut)
    part_b_summary(b_results)

    # ---- Part C ----
    c_results = part_c(eq_close, eq_open, de_index, spy, common, w_fut)
    part_c_summary(c_results)

    # ---- Part D ----
    d_results = part_d(eq_close, eq_open, de_index, spy, common, carry_rroll)
    part_d_summary(d_results)

    # ---- Part E ----
    e_results = part_e(eq_close, eq_open, de_index, spy, common, w_fut)
    part_e_summary(e_results)

    # ---- Decisions ----
    a_pass_25 = a_results["close_to_close_fut0.25"]["gates"]["all_passed"]
    a_pass_50 = a_results["close_to_close_fut0.50"]["gates"]["all_passed"]
    d_blend_beats = {k: v.get("beats_pure_tsm18m", False)
                     for k, v in d_results.items()
                     if k.startswith("blend_")}
    d_any_blend_beats = any(d_blend_beats.values())
    b_high = {w_f: b_results["high_20_5bps"][f"fut{w_f:.2f}"]["oos_sharpe"]
              for w_f in [0.25, 0.50]}
    promotion_survives = a_pass_25  # Part A gate is the promotion-critical test

    print("\n" + "=" * 72)
    print("E020 Decisions")
    print("=" * 72)
    print(f"  Part A (promotion-critical): convention-aligned gates "
          f"fut0.25={'PASS' if a_pass_25 else 'FAIL'}, "
          f"fut0.50={'PASS' if a_pass_50 else 'FAIL'}")
    print(f"  Part B: high-cost OOS Sharpe fut0.25={b_high[0.25]:.3f}, "
          f"fut0.50={b_high[0.50]:.3f} "
          f"(2.0 gate survives: "
          f"{b_results['high_20_5bps']['fut0.25']['high_cost_gate_survives']}/"
          f"{b_results['high_20_5bps']['fut0.50']['high_cost_gate_survives']})")
    c_grid = ", ".join(
        f"{lb}: {c_results[lb]['total']['oos_sharpe']:.3f}"
        for lb in ["9m", "12m", "18m"])
    print(f"  Part C: lookback grid ({c_grid})")
    print(f"  Part D: blend sleeve beats pure TSM-18m on total OOS: "
          f"{d_blend_beats}")
    print(f"  E019 promotion survives Part A: {'YES' if promotion_survives else 'NO'}")

    # ---- Save ----
    result = {
        "experiment": "E020",
        "timestamp": deterministic_timestamp(),
        "description": ("Robustness validation of the promoted E019 total "
                        "portfolio: (A) execution-convention alignment, "
                        "(B) cost sweep, (C) equity lookback sensitivity, "
                        "(D) futures-sleeve variant, (E) fine weight grid."),
        "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP},
        "rebalance_freq_days": REBAL,
        "pre_registered": {
            "part_a": {
                "test": ("re-run the total portfolio with the equity sleeve "
                         "on close-to-close returns (matching the futures "
                         "convention)"),
                "gates": {"oos_sharpe_gte_2.0": 2.0,
                          "bear_sharpe_gt_aligned_equity": ("strict inequality, "
                                                           "same convention")},
                "promotion_critical": True,
                "failure_consequence": ("promotion is convention-dependent - "
                                        "demote and record the negative"),
            },
            "part_b": {
                "test": ("cost sweep {base 0.5+0.2bps, high 20+5bps, zero} "
                         "on the promoted 25%/50% portfolios"),
                "gate": "measurement only (no promotion gate); record whether "
                        "the 2.0 gate survives high costs",
            },
            "part_c": {
                "test": ("equity lookback sensitivity {9, 12, 18}m at the "
                         "promoted 25% futures weight"),
                "gate": "sensitivity only (multiple-testing awareness); 12m is "
                        "the registered primary",
            },
            "part_d": {
                "test": ("futures-sleeve variant at the promoted 25% futures "
                         "weight: pure TSM-18m vs the Part-A-promoted blend "
                         "sleeve (TSM weight 0.5/0.7)"),
                "falsification": ("the blend sleeve must beat pure TSM-18m on "
                                  "TOTAL-portfolio OOS Sharpe at futures "
                                  "weight 0.25 to replace it"),
            },
            "part_e": {
                "test": ("fine futures-weight grid {0.10, 0.15, 0.20, 0.30, "
                         "0.40, 0.60} at the primary configuration"),
                "gate": "sensitivity only; the 0.25/0.50 cells are E019's "
                        "pre-registered cells",
            },
        },
        "premise_verification": {
            "step": ("prioritization v1.2.1 mandatory pre-registration step: "
                     "every factual premise in the E019 handoff verified "
                     "against experiments/e019_cross_asset_portfolio.json "
                     "before running"),
            "premises_checked": [
                "promoted total portfolios: fut0.25 OOS 2.175 / bear -0.516 / "
                "maxDD -0.243 / turnover 0.0602 / beta -0.051; fut0.50 OOS "
                "2.034 / bear +0.059 / maxDD -0.176 / turnover 0.0563 / "
                "beta -0.037 - MATCH the E019 JSON",
                "equity flagship (common calendar): OOS 2.157 / bear -0.816 / "
                "maxDD -0.313 / turnover 0.0640 / beta -0.065 - MATCHES",
                "TSM-18m sleeve OOS 0.805 and carry-252d OOS 0.523 anchors - "
                "MATCH",
                "Part-A blend grid: TSM weight 0.5 OOS 0.858 / 0.7 OOS 0.876 "
                "(both promoted) - MATCH",
                "turnover 6.0% at w=0.25 and the ~0.25-Sharpe high-cost drag "
                "estimate - consistent with the JSON turnover 0.0602",
            ],
            "corrections": "none - all premises verified",
        },
        "universe": {
            "futures": list(FUTURES_UNIVERSE.keys()),
            "futures_pairs": {k: v[0] for k, v in FUTURES_UNIVERSE.items()},
            "equity": "large_liquid",
            "equity_n_tickers": int(eq_close.shape[1]),
            "equity_missing": [t for t in UNIVERSES["large_liquid"]
                               if t not in eq_close_full.columns],
            "n_common_days": int(len(common)),
            "start": str(common[0].date()),
            "end": str(common[-1].date()),
        },
        "e019_replication": {
            key: {k: v for k, v in res.items() if k != "fold_metrics"}
            for key, res in replication.items()
        },
        "e019_replication_check": {
            key: {
                "computed_oos_sharpe": replication[key]["oos_sharpe"],
                "e019_recorded": anchor,
                "delta": replication[key]["oos_sharpe"] - anchor,
                "replicated": bool(abs(replication[key]["oos_sharpe"] - anchor) < E019_ANCHOR_TOL),
            }
            for key, anchor in E019_ANCHOR_VALUES.items()
        },
        "inter_sleeve_correlation": float(eq_ret["net"].corr(fut_ret["net"])),
        "part_a": {k: {kk: vv for kk, vv in v.items() if kk != "fold_metrics"}
                   for k, v in a_results.items()},
        "part_b": {
            name: {
                "cost_scenario": row["cost_scenario"],
                "tc_cost": row["tc_cost"],
                "slippage": row["slippage"],
                "fut0.25": {k: v for k, v in row["fut0.25"].items()
                              if k != "fold_metrics"},
                "fut0.50": {k: v for k, v in row["fut0.50"].items()
                              if k != "fold_metrics"},
            }
            for name, row in b_results.items()
        },
        "part_c": {
            lb: {
                "equity_only": {k: v for k, v in v["equity_only"].items()
                                if k != "fold_metrics"},
                "total": {k: v for k, v in v["total"].items()
                          if k != "fold_metrics"},
            }
            for lb, v in c_results.items()
        },
        "part_d": {
            name: {
                "sleeve_standalone": {k: v for k, v in v["sleeve_standalone"].items()
                                      if k != "fold_metrics"},
                "total": {k: v for k, v in v["total"].items()
                          if k != "fold_metrics"},
                **({"beats_pure_tsm18m": v["beats_pure_tsm18m"],
                    "gates": v["gates"]} if "gates" in v else {}),
            }
            for name, v in d_results.items()
        },
        "part_e": {k: {kk: vv for kk, vv in v.items() if kk != "fold_metrics"}
                   for k, v in e_results.items()},
        "decisions": {
            "part_a_pass_fut0.25": a_pass_25,
            "part_a_pass_fut0.50": a_pass_50,
            "part_d_blend_beats_pure": d_blend_beats,
            "part_d_any_blend_beats_pure": d_any_blend_beats,
            "part_b_high_cost_oos": {str(k): v for k, v in b_high.items()},
            "e019_promotion_survives": promotion_survives,
        },
    }

    out_path = os.path.join("experiments", "e020_robustness.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        jsonio.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
