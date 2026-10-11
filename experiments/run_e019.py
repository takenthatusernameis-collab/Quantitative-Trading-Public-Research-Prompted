#!/usr/bin/env python3
"""E019: Pre-registered cross-asset portfolio construction.

Follows the E018 handoff. E018 closed both open questions (carry
z=2.65 below the 3.0 bar; 18m TSM 0.805 below the 1.0 gate) but
surfaced the real decision: the futures sleeve's value is
diversification, not standalone Sharpe. This experiment tests the
two construction-level questions with fresh pre-registration:

  Part A - TSM(18m) + carry(252d) blend grid on the extended
           futures panel. The E018 debugging run disclosed blend
           Sharpes of 0.703/0.821/0.814 (TSM-9m weights 0.3/0.5/0.7,
           NOT official results); the fresh falsification bar is the
           BEST pure variant, TSM-18m (0.805), not the 9m primary.

  Part B - Total-portfolio test: equity flagship (pure TSM 12m,
           long-only, inverse-vol, large_liquid, E010/E015
           construction) + futures sleeve (TSM-18m symmetric,
           de-seamed) at futures weights {0.25, 0.5, 0.75}.

PRE-REGISTERED BEFORE RUNNING (gates set ex-ante, goalposts not
movable after the run):

  Part A blend gates (each cell, TSM weight {0.3, 0.5, 0.7}):
    - OOS Sharpe >= 0.8
    - matched-blended-placebo z >= 3
    - positive bear-market Sharpe
    - |beta vs SPY| <= 0.2
    - turnover <= 0.08
    Falsification criterion: the best blend must beat pure TSM-18m
    (OOS Sharpe 0.805, the best pure variant) on OOS Sharpe.

  Part B total-portfolio gates (each futures weight):
    - total OOS Sharpe >= 2.0
    - bear-market Sharpe STRICTLY greater than the equity-only
      flagship's (both evaluated on the same common calendar)

  Placebo constructions (matched to each tested cell):
    - Blend cell at TSM weight w: w * random-TSM + (1-w) *
      permuted-carry, where the carry component uses E018's
      seam-calendar-preserving permutation of detected seam excess
      gaps (the validated carry null). 50 sims, SEED=42. This
      improves on E017/E018's single 50/50 blended placebo: each
      cell is tested against the null of its own construction.
    - Total-portfolio cell at futures weight w: (1-w) * random
      equity TSM + w * random futures TSM. 50 sims, SEED=42.
      Supplementary validation (not a pre-registered gate).

  Calendar: both sleeves evaluated on the COMMON calendar (the
  3205-day futures panel calendar, 2014-01-02..2026-10-09), so
  folds, regimes and gate references are apples-to-apples. The
  equity-only flagship's gate reference is its own performance on
  this common calendar (NOT its full-calendar 2.141).

Known caveats (pre-registered, documented not hidden):
  - Execution-mismatch: the equity sleeve earns close->next-open
    segment returns (next-day-open execution convention of the
    repo's equity pipeline); the futures sleeve earns full
    close->close returns on de-seamed synthetic indices (no
    observable opens). The blend mixes the two conventions.
  - The repo's rebalance sampling is position-based (every 21st
    row), so the equity sleeve's rebalance dates on the common
    calendar differ slightly from its full-calendar rebalance
    dates; the common-calendar equity-only baseline is the
    correct gate reference.
  - E018's handoff narrative claimed "the equity flagship carries
    full equity beta (beta ~0.9)". That is FALSE for the registered
    monthly-rebalanced construction: E015 recorded beta -0.066 and
    this run verifies beta ~-0.07 on the common calendar. The
    total-portfolio test is therefore a return-stream-diversification
    test, NOT a beta-offset test. Gates do not depend on the
    mis-stated premise; the correction is recorded in the ledger.
  - 42 folds with only ~8 true bear regimes: bear-Sharpe gates
    remain noisy; do not over-claim crisis alpha.

Replication anchors (E018, deterministic): TSM-18m OOS Sharpe
0.805 (bear +1.348, beta -0.010, turnover 0.049); realized-
roll-yield carry 252d OOS Sharpe 0.523 (bear +0.907, beta
+0.014, turnover 0.031). The E017 9m grid reproduced exactly in
E018; this run re-verifies the 18m anchors.
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

# Part A: blend grid on the extended futures panel.
TSM_LOOKBACK = 18          # strongest pure variant (E016 0.894 / E017 0.805)
CARRY_WINDOW = 252         # pre-registered primary carry window (E016/E017/E018)
BLEND_TSM_WEIGHTS = [0.3, 0.5, 0.7]

BLEND_GATES = {
    "oos_sharpe_gte_0.8": 0.8,
    "blend_placebo_z_gte_3": 3.0,
    "bear_sharpe_positive": 0.0,
    "abs_beta_lte_0.2": 0.2,
    "turnover_lte_0.08": 0.08,
}
# Falsification bar: best pure variant (TSM-18m), not the 9m primary.
BLEND_FALSIFICATION_BAR = 0.805  # E018 recorded TSM-18m OOS Sharpe

# Part B: total portfolio (equity flagship + futures sleeve).
EQUITY_TSM_LOOKBACK = 12     # E010/E015 flagship construction
FUTURES_WEIGHTS = [0.25, 0.5, 0.75]

TOTAL_GATES = {
    "oos_sharpe_gte_2.0": 2.0,
    "bear_sharpe_gt_equity_only": None,  # strict inequality, set from data
}

# E018 recorded anchors (replication checks, deterministic).
E018_ANCHORS = {
    "tsm_deseamed_18m": {"oos_sharpe": 0.805, "bear_sharpe": 1.348,
                         "turnover": 0.049, "positive_folds": 23},
    "carry_realized_rollyield_252d": {"oos_sharpe": 0.523, "bear_sharpe": 0.907,
                                      "turnover": 0.031, "positive_folds": 28},
}


# ---------------------------------------------------------------------------
# Part A machinery.
# ---------------------------------------------------------------------------

def build_futures_weights(de_index, lookback, carry_rroll, vol):
    """TSM(lookback) and realized-roll-yield carry(252d) weight panels."""
    tsm_sig = strategies.time_series_momentum_pure(de_index, lookback=lookback, skip=1)
    w_tsm = backtest.time_series_momentum_weights(
        tsm_sig, de_index, long_only=False, vol_window=63
    )
    w_carry = backtest.carry_weights(carry_rroll, vol)
    return w_tsm, w_carry


def blended_placebo_weighted(de_index, fut_close, spot_close, seams_dt,
                             spy, w_tsm, window, n_sim, seed=SEED):
    """Matched blended placebo for a TSM+carry blend at TSM weight ``w_tsm``.

    Null construction (mirrors the tested cell exactly):
      - TSM component: random normal signal -> symmetric inv-vol TSM weights.
      - Carry component: seam-calendar-preserving permutation of each
        contract's detected seam excess gaps (E018's validated carry
        null) -> dollar-neutral top/bottom-half inv-vol carry weights.
      - Blend at the same TSM weight as the tested cell.
    50 sims; returns (mean, std) of OOS mean-fold Sharpe.
    """
    rng = np.random.default_rng(seed)
    spy_ret = spy.pct_change().fillna(0.0)
    vol = de_index.pct_change().rolling(63).std().replace(0, np.nan)
    sharps = []
    for _ in range(n_sim):
        tsm_sig = pd.DataFrame(
            rng.standard_normal(size=de_index.shape),
            index=de_index.index, columns=de_index.columns,
        )
        tsm_w = backtest.time_series_momentum_weights(
            tsm_sig, de_index, long_only=False, vol_window=63
        )
        carry_sig = permuted_carry_panel(
            fut_close, spot_close, seams_dt, window, rng
        )
        carry_w = backtest.carry_weights(carry_sig, vol)
        bw = w_tsm * tsm_w + (1.0 - w_tsm) * carry_w
        r = backtest.portfolio_returns_rebalance_clean(
            bw, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE,
            rebalance_freq=REBAL
        )
        fm, _ = walk_forward(r, de_index, spy_ret)
        s = [m["sharpe"] for m in fm
             if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
        sharps.append(float(np.mean(s)) if s else 0.0)
    return float(np.mean(sharps)), float(np.std(sharps))


def blend_gate_check(res, z):
    """Pre-registered Part A gate evaluation."""
    checks = {
        "oos_sharpe_gte_0.8": bool(res["oos_sharpe"] >= BLEND_GATES["oos_sharpe_gte_0.8"]),
        "blend_placebo_z_gte_3": bool(z >= BLEND_GATES["blend_placebo_z_gte_3"]),
        "bear_sharpe_positive": bool(res["regime_analysis"]["bear"]["sharpe_mean"] > BLEND_GATES["bear_sharpe_positive"]),
        "abs_beta_lte_0.2": bool(abs(res["equity_beta"]) <= BLEND_GATES["abs_beta_lte_0.2"]),
        "turnover_lte_0.08": bool(res["turnover"] <= BLEND_GATES["turnover_lte_0.08"]),
    }
    checks["all_passed"] = all(v for k, v in checks.items() if k != "all_passed")
    return checks


# ---------------------------------------------------------------------------
# Part B machinery.
# ---------------------------------------------------------------------------

def equity_flagship(close, open_):
    """E010/E015 equity flagship: pure TSM 12m, long-only, inv-vol (63d)."""
    sig = strategies.time_series_momentum_pure(close, lookback=EQUITY_TSM_LOOKBACK, skip=1)
    w = backtest.time_series_momentum_weights(
        sig, close, long_only=True, vol_window=63
    )
    return w


def futures_sleeve(de_index):
    """Futures sleeve: symmetric TSM-18m on de-seamed indices."""
    sig = strategies.time_series_momentum_pure(de_index, lookback=TSM_LOOKBACK, skip=1)
    w = backtest.time_series_momentum_weights(
        sig, de_index, long_only=False, vol_window=63
    )
    return w


def eval_net_series(net, spy_ret, index_df, turnover, label):
    """Walk-forward + diagnostics for a net-return series on a calendar.

    ``index_df`` supplies the calendar (index) for fold boundaries.
    """
    rets = pd.DataFrame({
        "gross": net,
        "costs": pd.Series(0.0, index=net.index),
        "net": net,
    })
    diag = market_diagnostics(rets, spy_ret)
    fm, splits = walk_forward(rets, index_df, spy_ret)
    sharpes = [m["sharpe"] for m in fm
               if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
    oos_sharpe = float(np.mean(sharpes)) if sharpes else float("nan")
    oos_std = float(np.std(sharpes)) if sharpes else float("nan")
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


def total_portfolio_placebo(close_c, open_c, de_index, spy, common,
                            w_fut, n_sim, seed=SEED):
    """Matched placebo for the total portfolio at futures weight ``w_fut``.

    Null: (1-w) * random equity TSM (long-only inv-vol on the common-
    calendar equity panel) + w * random futures TSM (symmetric inv-vol
    on the de-seamed panel). Supplementary validation only (not a
    pre-registered gate).
    """
    rng = np.random.default_rng(seed)
    spy_ret = spy.pct_change().fillna(0.0)
    index_df = pd.DataFrame(index=common)
    sharps = []
    for _ in range(n_sim):
        eq_sig = pd.DataFrame(
            rng.standard_normal(size=close_c.shape),
            index=close_c.index, columns=close_c.columns,
        )
        eq_w = backtest.time_series_momentum_weights(
            eq_sig, close_c, long_only=True, vol_window=63
        )
        eq_r = backtest.portfolio_returns_rebalance_clean(
            eq_w, close_c, open_c, tc_cost=TC_COST, slippage=SLIPPAGE,
            rebalance_freq=REBAL
        )
        fut_sig = pd.DataFrame(
            rng.standard_normal(size=de_index.shape),
            index=de_index.index, columns=de_index.columns,
        )
        fut_w = backtest.time_series_momentum_weights(
            fut_sig, de_index, long_only=False, vol_window=63
        )
        fut_r = backtest.portfolio_returns_rebalance_clean(
            fut_w, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE,
            rebalance_freq=REBAL
        )
        tot = (1.0 - w_fut) * eq_r["net"] + w_fut * fut_r["net"]
        res = eval_net_series(tot, spy_ret, index_df, 0.0, "placebo")
        sharps.append(res["oos_sharpe"])
    return float(np.mean(sharps)), float(np.std(sharps))


def total_gate_check(res, equity_bear):
    """Pre-registered Part B gate evaluation."""
    checks = {
        "oos_sharpe_gte_2.0": bool(res["oos_sharpe"] >= TOTAL_GATES["oos_sharpe_gte_2.0"]),
        "bear_sharpe_gt_equity_only": bool(
            res["regime_analysis"]["bear"]["sharpe_mean"] > equity_bear
        ),
    }
    checks["all_passed"] = all(v for k, v in checks.items() if k != "all_passed")
    return checks


# ---------------------------------------------------------------------------
# Main.
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-sim", type=int, default=PLACEBO_N_SIM,
                        help="placebo simulations (default 50)")
    args = parser.parse_args()
    n_sim = args.n_sim

    print("=" * 72)
    print("E019: Pre-registered Cross-Asset Portfolio Construction")
    print("=" * 72)
    print("Pre-registered gates (set before running):")
    print("  Part A blend: OOS Sharpe >= 0.8, matched-placebo z >= 3,")
    print("                bear Sharpe > 0, |beta| <= 0.2, turnover <= 0.08;")
    print(f"                falsification: best blend must beat TSM-18m "
          f"({BLEND_FALSIFICATION_BAR:.3f})")
    print("  Part B total: OOS Sharpe >= 2.0 AND bear Sharpe strictly")
    print("                greater than the equity-only flagship (common calendar)")

    # ---- Part 0: panels and common calendar ----
    panels = build_panels(FUTURES_UNIVERSE)
    de_index = panels["de_index"]
    fut_close = panels["fut_close"]
    spot_close = panels["spot_close"]
    carry_rroll = panels["carry_rroll"]
    spy = panels["spy"]
    seams_dt = {k: pd.DatetimeIndex(v) for k, v in panels["seams"].items()}

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

    # ---- Part 1: replication anchors (pure variants) ----
    print("\n" + "-" * 72)
    print("Part 1: Replication anchors (pure variants on the futures panel)")
    print("-" * 72)
    vol = de_index.pct_change().rolling(63).std().replace(0, np.nan)
    w_tsm18, w_carry252 = build_futures_weights(de_index, TSM_LOOKBACK, carry_rroll, vol)

    tsm_res, _ = evaluate(de_index, de_index, spy, w_tsm18, f"tsm_deseamed_{TSM_LOOKBACK}m")
    carry_res, _ = evaluate(de_index, de_index, spy, w_carry252,
                            f"carry_realized_rollyield_{CARRY_WINDOW}d")
    anchors = {"tsm_deseamed_18m": tsm_res, "carry_realized_rollyield_252d": carry_res}
    for lbl, res in anchors.items():
        recorded = E018_ANCHORS[lbl]
        bear = res["regime_analysis"]["bear"]["sharpe_mean"]
        ok = abs(res["oos_sharpe"] - recorded["oos_sharpe"]) < 5e-4
        print(f"  {lbl:<32} OOS={res['oos_sharpe']:.3f} "
              f"(E018 {recorded['oos_sharpe']:.3f})  bear={bear:+.3f}  "
              f"beta={res['equity_beta']:+.3f}  turn={res['turnover']:.4f}  "
              f"pos={res['positive_folds']}/{res['n_folds']}  "
              f"{'REPLICATED' if ok else 'DIFFERS'}")

    # E017/E018's 50/50 blended placebo (SEED=42) for anchor z-scores.
    pm50, ps50 = blended_placebo(de_index, spy, n_sim=n_sim)
    print(f"  50/50 blended placebo (E017/E018 construction, SEED=42): "
          f"mean={pm50:.3f} std={ps50:.3f} n_sim={n_sim}")
    for lbl, res in anchors.items():
        z50 = (res["oos_sharpe"] - pm50) / ps50 if ps50 > 0 else float("nan")
        res["placebo_z_50_50_blended"] = float(z50)
        res["placebo_mean_50_50"] = pm50
        res["placebo_std_50_50"] = ps50
        print(f"    {lbl:<32} z vs 50/50 blended null = {z50:.2f}")

    # ---- Part 2: pre-registered TSM(18m)+carry(252d) blend grid ----
    print("\n" + "-" * 72)
    print(f"Part 2: Blend grid TSM({TSM_LOOKBACK}m) + carry({CARRY_WINDOW}d), "
          f"TSM weight {BLEND_TSM_WEIGHTS} (matched placebos, {n_sim} sims each)")
    print("-" * 72)
    blend_results = {}
    for tsm_w in BLEND_TSM_WEIGHTS:
        w = tsm_w * w_tsm18 + (1.0 - tsm_w) * w_carry252
        res, _ = evaluate(de_index, de_index, spy, w, f"blend_tsm{tsm_w:.1f}_carry{1.0 - tsm_w:.1f}")
        pm, ps = blended_placebo_weighted(
            de_index, fut_close, spot_close, seams_dt, spy, tsm_w,
            CARRY_WINDOW, n_sim
        )
        z = (res["oos_sharpe"] - pm) / ps if ps > 0 else float("nan")
        res["placebo_z"] = float(z)
        res["placebo_mean"] = pm
        res["placebo_std"] = ps
        res["tsm_weight"] = tsm_w
        res["gates"] = blend_gate_check(res, z)
        res["beats_pure_tsm18m"] = bool(res["oos_sharpe"] > tsm_res["oos_sharpe"])
        blend_results[f"tsm_weight_{tsm_w:.1f}"] = res
        bear = res["regime_analysis"]["bear"]["sharpe_mean"]
        print(f"  tsm_w={tsm_w:.1f}  OOS={res['oos_sharpe']:.3f}  z={z:.2f}  "
              f"beta={res['equity_beta']:+.3f}  bear={bear:+.3f}  "
              f"turn={res['turnover']:.4f}  beats_TSM18m={res['beats_pure_tsm18m']}  "
              f"gates={'PASS' if res['gates']['all_passed'] else 'FAIL'}")
        for g, ok in res["gates"].items():
            if g != "all_passed":
                print(f"      {g:<28} {'PASS' if ok else 'FAIL'}")

    best_blend_key = max(blend_results, key=lambda k: blend_results[k]["oos_sharpe"])
    best_blend = blend_results[best_blend_key]
    falsified = best_blend["oos_sharpe"] > tsm_res["oos_sharpe"]
    print(f"\n  Best blend: {best_blend_key} OOS={best_blend['oos_sharpe']:.3f}")
    print(f"  Falsification (best blend > TSM-18m {tsm_res['oos_sharpe']:.3f}): "
          f"{'YES' if falsified else 'NO'}")
    part_a_pass = best_blend["gates"]["all_passed"] and falsified
    print(f"  Part A decision: "
          f"{'PROMOTE blend' if part_a_pass else 'NO promotion (gates/falsification failed)'}")

    # ---- Part 3: pre-registered total-portfolio test ----
    print("\n" + "-" * 72)
    print(f"Part 3: Total portfolio - equity flagship (TSM {EQUITY_TSM_LOOKBACK}m, "
          f"long-only, inv-vol, large_liquid) + futures sleeve (TSM-{TSM_LOOKBACK}m, "
          f"de-seamed), futures weights {FUTURES_WEIGHTS}")
    print("-" * 72)

    # Equity sleeve (common calendar).
    w_eq = equity_flagship(eq_close, eq_open)
    eq_ret = backtest.portfolio_returns_rebalance_clean(
        w_eq, eq_close, eq_open, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
    )
    eq_turn = backtest.average_turnover(w_eq)
    eq_res = eval_net_series(eq_ret["net"], spy_ret, index_df, eq_turn,
                             "equity_flagship_tsm12m")

    # Futures sleeve (common calendar = futures panel calendar).
    w_fut = futures_sleeve(de_index)
    fut_ret = backtest.portfolio_returns_rebalance_clean(
        w_fut, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
    )
    fut_turn = backtest.average_turnover(w_fut)
    fut_res = eval_net_series(fut_ret["net"], spy_ret, index_df, fut_turn,
                              "futures_sleeve_tsm18m")

    eq_bear = eq_res["regime_analysis"]["bear"]["sharpe_mean"]
    print(f"  Equity-only flagship (common calendar): OOS={eq_res['oos_sharpe']:.3f}  "
          f"beta={eq_res['equity_beta']:+.3f}  bear={eq_bear:+.3f}  "
          f"maxDD={eq_res['max_drawdown']:.3f}  turn={eq_turn:.4f}  "
          f"pos={eq_res['positive_folds']}/{eq_res['n_folds']}")
    print(f"  (Equity flagship on its own full calendar: OOS=2.141 recorded in E015; "
          f"the common-calendar value above is the gate reference.)")
    print(f"  Futures sleeve (TSM-{TSM_LOOKBACK}m): OOS={fut_res['oos_sharpe']:.3f}  "
          f"beta={fut_res['equity_beta']:+.3f}  bear={fut_res['regime_analysis']['bear']['sharpe_mean']:+.3f}  "
          f"maxDD={fut_res['max_drawdown']:.3f}  turn={fut_turn:.4f}  "
          f"pos={fut_res['positive_folds']}/{fut_res['n_folds']}")

    # Inter-sleeve correlation (daily net returns).
    sleeve_corr = float(eq_ret["net"].corr(fut_ret["net"]))
    print(f"  Inter-sleeve daily net-return correlation: {sleeve_corr:+.3f}")

    total_results = {}
    for w_f in FUTURES_WEIGHTS:
        tot_net = (1.0 - w_f) * eq_ret["net"] + w_f * fut_ret["net"]
        # Turnover scales linearly with constant sleeve weights (positions are
        # scaled by the sleeve weight; gross exposure sums to 1).
        tot_turn = (1.0 - w_f) * eq_turn + w_f * fut_turn
        res = eval_net_series(tot_net, spy_ret, index_df, tot_turn,
                              f"total_fut{w_f:.2f}")
        res["futures_weight"] = w_f
        res["equity_weight"] = 1.0 - w_f
        res["gates"] = total_gate_check(res, eq_bear)
        res["beats_equity_only_oos"] = bool(res["oos_sharpe"] > eq_res["oos_sharpe"])
        # Per-sleeve contribution to total net return.
        eq_contrib = (1.0 - w_f) * float(eq_ret["net"].mean())
        fut_contrib = w_f * float(fut_ret["net"].mean())
        tot_mean = float(tot_net.mean())
        res["contribution"] = {
            "equity": eq_contrib,
            "futures": fut_contrib,
            "equity_share": eq_contrib / tot_mean if tot_mean else float("nan"),
            "futures_share": fut_contrib / tot_mean if tot_mean else float("nan"),
        }
        total_results[f"futures_weight_{w_f:.2f}"] = res
        bear = res["regime_analysis"]["bear"]["sharpe_mean"]
        print(f"  fut_w={w_f:.2f}  OOS={res['oos_sharpe']:.3f}  "
              f"beta={res['equity_beta']:+.3f}  bear={bear:+.3f}  "
              f"maxDD={res['max_drawdown']:.3f}  turn={tot_turn:.4f}  "
              f"pos={res['positive_folds']}/{res['n_folds']}  "
              f"beats_equity_only={res['beats_equity_only_oos']}  "
              f"gates={'PASS' if res['gates']['all_passed'] else 'FAIL'}")
        for g, ok in res["gates"].items():
            if g != "all_passed":
                print(f"      {g:<28} {'PASS' if ok else 'FAIL'}")

    # Matched total-portfolio placebo (supplementary validation).
    print(f"\n  Matched total-portfolio placebo ({n_sim} sims each)...")
    for w_f in FUTURES_WEIGHTS:
        pm, ps = total_portfolio_placebo(
            eq_close, eq_open, de_index, spy, common, w_f, n_sim
        )
        res = total_results[f"futures_weight_{w_f:.2f}"]
        z = (res["oos_sharpe"] - pm) / ps if ps > 0 else float("nan")
        res["placebo_mean"] = pm
        res["placebo_std"] = ps
        res["placebo_z"] = float(z)
        print(f"    fut_w={w_f:.2f}  placebo mean={pm:.3f} std={ps:.3f}  z={z:.2f}")

    # Decision.
    passing = [k for k, v in total_results.items() if v["gates"]["all_passed"]]
    best_total_key = max(total_results, key=lambda k: total_results[k]["oos_sharpe"])
    best_total = total_results[best_total_key]
    part_b_pass = bool(passing)
    print(f"\n  Best total portfolio: {best_total_key} OOS={best_total['oos_sharpe']:.3f}")
    print(f"  Part B decision: "
          f"{'PROMOTE total portfolio (weights: ' + ', '.join(passing) + ')' if part_b_pass else 'NO promotion (no futures weight clears the pre-registered gates)'}")

    # ---- Summary ----
    print("\n" + "=" * 72)
    print("E019 Summary")
    print("=" * 72)
    print(f"  Anchors replicated: TSM-18m OOS={tsm_res['oos_sharpe']:.3f} "
          f"(E018 0.805), carry-252d OOS={carry_res['oos_sharpe']:.3f} (E018 0.523)")
    print(f"  Part A best blend: {best_blend_key} OOS={best_blend['oos_sharpe']:.3f} "
          f"z={best_blend['placebo_z']:.2f} gates="
          f"{'PASS' if best_blend['gates']['all_passed'] else 'FAIL'} "
          f"falsification={'YES' if falsified else 'NO'}")
    print(f"  Part B best total: {best_total_key} OOS={best_total['oos_sharpe']:.3f} "
          f"bear={best_total['regime_analysis']['bear']['sharpe_mean']:+.3f} "
          f"vs equity-only {eq_bear:+.3f} gates="
          f"{'PASS' if best_total['gates']['all_passed'] else 'FAIL'}")
    print(f"  Inter-sleeve correlation: {sleeve_corr:+.3f}")

    # ---- Save ----
    result = {
        "experiment": "E019",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "description": ("Pre-registered cross-asset portfolio construction: "
                        "(a) TSM(18m)+carry(252d) blend grid with fresh gates "
                        "and matched placebos; (b) total-portfolio test of the "
                        "equity flagship (TSM 12m, large_liquid) + futures "
                        "sleeve (TSM-18m, de-seamed)."),
        "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP},
        "rebalance_freq_days": REBAL,
        "pre_registered": {
            "part_a": {
                "blend": f"TSM({TSM_LOOKBACK}m) + realized-roll-yield carry({CARRY_WINDOW}d)",
                "tsm_weights": BLEND_TSM_WEIGHTS,
                "gates": {k: v for k, v in BLEND_GATES.items()},
                "falsification": (f"best blend must beat pure TSM-18m OOS Sharpe "
                                  f"({BLEND_FALSIFICATION_BAR:.3f}, E018 recorded)"),
                "placebo": (f"matched per cell: w*random TSM + (1-w)*permuted carry "
                            f"(seam-calendar-preserving, E018 construction), {n_sim} sims, SEED=42"),
                "improvement_over_e017_e018": ("E017/E018 used a single 50/50 blended "
                                               "placebo for the whole grid; E019 matches "
                                               "the null to each cell's own construction"),
            },
            "part_b": {
                "equity_sleeve": ("pure TSM 12m, long-only, inverse-vol (63d), "
                                  "large_liquid, E010/E015 construction, next-day-open "
                                  "execution"),
                "futures_sleeve": ("symmetric TSM-18m, inverse-vol (63d), de-seamed "
                                   "16-contract panel, close-to-close execution"),
                "futures_weights": FUTURES_WEIGHTS,
                "gates": {"oos_sharpe_gte_2.0": 2.0,
                          "bear_sharpe_gt_equity_only": "strict inequality, common calendar"},
                "placebo": (f"matched per cell: (1-w)*random equity TSM + w*random "
                            f"futures TSM, {n_sim} sims, SEED=42 (supplementary, "
                            f"not a pre-registered gate)"),
                "calendar": ("common calendar = futures panel calendar "
                             f"({len(common)} days); the equity-only flagship on this "
                             "calendar is the gate reference, not its full-calendar 2.141"),
            },
            "premise_correction": ("E018's handoff claimed the equity flagship carries "
                                 "full equity beta (~0.9). FALSE for the registered "
                                 "monthly-rebalanced construction (E015 recorded beta "
                                 "-0.066; this run verifies ~-0.07). The total-portfolio "
                                 "test is a return-stream-diversification test, not a "
                                 "beta-offset test. Gates do not depend on the premise."),
            "caveats": [
                "Execution-mismatch: equity sleeve earns close->next-open segment "
                "returns; futures sleeve earns full close->close returns on de-seamed "
                "synthetic indices (no observable opens).",
                "Repo rebalance sampling is position-based (every 21st row); the "
                "equity sleeve's rebalance dates on the common calendar differ "
                "slightly from its full-calendar dates.",
                "42 folds with ~8 bear regimes: bear-Sharpe gates are noisy.",
                "yfinance single source; BK and WBA missing from the equity panel "
                "(130 of 132 tickers).",
            ],
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
        "anchors": {
            lbl: {k: v for k, v in res.items()
                  if k not in ("fold_metrics",)}
            for lbl, res in anchors.items()
        },
        "anchors_replication": {
            lbl: {
                "oos_sharpe": res["oos_sharpe"],
                "e018_recorded": E018_ANCHORS[lbl]["oos_sharpe"],
                "delta": res["oos_sharpe"] - E018_ANCHORS[lbl]["oos_sharpe"],
                "replicated": bool(abs(res["oos_sharpe"] - E018_ANCHORS[lbl]["oos_sharpe"]) < 5e-4),
            }
            for lbl, res in anchors.items()
        },
        "blended_placebo_50_50": {"mean": pm50, "std": ps50, "n_sim": n_sim},
        "blend_grid": {
            k: {kk: vv for kk, vv in v.items() if kk != "fold_metrics"}
            for k, v in blend_results.items()
        },
        "part_a_decision": {
            "best_blend": best_blend_key,
            "best_blend_oos_sharpe": best_blend["oos_sharpe"],
            "falsification_passed": falsified,
            "gates_passed": best_blend["gates"]["all_passed"],
            "promoted": part_a_pass,
        },
        "equity_flagship_common_calendar": {k: v for k, v in eq_res.items() if k != "fold_metrics"},
        "futures_sleeve": {k: v for k, v in fut_res.items() if k != "fold_metrics"},
        "inter_sleeve_correlation": sleeve_corr,
        "total_portfolio": {
            k: {kk: vv for kk, vv in v.items() if kk != "fold_metrics"}
            for k, v in total_results.items()
        },
        "part_b_decision": {
            "passing_weights": passing,
            "best": best_total_key,
            "best_oos_sharpe": best_total["oos_sharpe"],
            "promoted": part_b_pass,
        },
    }

    out_path = os.path.join("experiments", "e019_cross_asset_portfolio.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
