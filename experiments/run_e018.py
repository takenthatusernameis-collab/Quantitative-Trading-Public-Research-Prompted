#!/usr/bin/env python3
"""E018: Validation of realized-roll-yield carry (standalone) and a
pre-registered confirmatory run of 18m TSM.

Follows up the E017 handoff. E017 left carry's fate open: on the
extended 2014-2026 panel the realized-roll-yield variant reached
OOS Sharpe 0.523, z=2.80 against a *blended* TSM+carry placebo,
the repo's best bear-market Sharpe (+0.907) and lowest turnover
(3.1%) - just below the z=3 bar. E018 decides cleanly whether it
is a real component or a near-miss artifact before any portfolio
integration work.

Pre-registered design (fixed before running):

1. Carry-specific placebo null: 50 sims of random realized-roll-yield
   signals. The placebo preserves the seam calendar: each contract's
   detected seam excess gaps (futures-vs-spot return differences at
   seam dates) are randomly permuted across that contract's seam
   dates only, then the same trailing-window realized-roll-yield
   construction is applied. This keeps the number of seam events,
   their calendar positions and the per-contract gap-magnitude
   distribution, but destroys any timing relationship between
   accumulated roll yield and subsequent returns. (Identity
   permutation reproduces futures.realized_roll_yield exactly -
   asserted in the run.)
2. Carry gate (set before running): OOS Sharpe >= 0.5, carry-specific
   placebo z >= 3, positive bear Sharpe, |beta| <= 0.2,
   turnover <= 0.05.
3. Roll-yield window sensitivity {126, 252, 504} days; 252d is the
   pre-registered primary (unchanged from E016/E017), the others are
   sensitivity only. Each window gets its own 50-sim carry placebo.
4. Per-contract carry decomposition: standalone per-contract carry
   timing (long when the contract's own roll yield is positive /
   backwardated, short when negative), inverse-vol weighted - the
   mechanism-level test of KMPV carry. Reports per-contract OOS
   Sharpe, positive folds, mean roll-yield level and signal-vs-
   forward-return correlation (backwardation/contango plausibility).
5. TSM 18m pre-registered confirmatory run: 18m is the only lookback
   top-2 on BOTH the E016 short sample (0.894) and the E017 extended
   sample (0.805); selected from that two-sample evidence, not by
   maximizing the extended-sample Sharpe. Gate bar identical to E017:
   OOS Sharpe >= 1.0, placebo z >= 3, positive bear Sharpe,
   |beta| <= 0.2. The E017 primary (9m) remains the registered
   result; the full {6,9,12,18}m grid is reported with multiple-
   testing awareness.
6. Blend grid (conditional): runs ONLY if carry clears all its gates.
   TSM(9m primary) + realized-roll-yield carry(252d) at TSM weight
   {0.3, 0.5, 0.7}, pre-registered. Falsification criterion: at
   least one blend must beat pure TSM-9m (OOS Sharpe 0.680 on the
   extended panel) or carry adds nothing to the book.

Replication anchor: the E017 9m strategy grid is re-run first and
compared to E017's recorded numbers (the repo's bit-reproducibility
discipline; SEED=42 placebos are deterministic).
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import data, backtest, strategies, futures
from run_e017 import (
    build_panels, evaluate, walk_forward, blended_placebo, strategy_grid,
    FUTURES_UNIVERSE, TC_COST, SLIPPAGE, TRAIN, TEST, STEP, REBAL, SEED,
    PLACEBO_N_SIM, START,
)

# Pre-registered primary roll-yield window (unchanged from E016/E017).
PRIMARY_WINDOW = 252
WINDOWS = [126, 252, 504]

# Pre-registered confirmatory TSM lookback (see module docstring).
TSM_CONFIRMATORY_LOOKBACK = 18
TSM_LOOKBACK_GRID = [6, 9, 12, 18]

# Pre-registered carry gates (set before running).
CARRY_GATES = {
    "oos_sharpe_gte_0.5": 0.5,
    "carry_placebo_z_gte_3": 3.0,
    "bear_sharpe_positive": 0.0,
    "abs_beta_lte_0.2": 0.2,
    "turnover_lte_0.05": 0.05,
}

# Pre-registered TSM-18m gates (identical to E017).
TSM_GATES = {
    "oos_sharpe_gte_1.0": 1.0,
    "placebo_z_gte_3": 3.0,
    "bear_sharpe_positive": 0.0,
    "abs_beta_lte_0.2": 0.2,
}

# Pre-registered blend grid (conditional on carry clearing its gates).
BLEND_TSM_WEIGHTS = [0.3, 0.5, 0.7]
# Falsification bar: pure TSM-9m OOS Sharpe on the extended panel (E017).
BLEND_FALSIFICATION_BAR = 0.680

# E017's recorded 9m-grid numbers (replication anchor).
E017_RECORDED = {
    "tsm_raw_stitched": {"oos_sharpe": 0.225, "bear_sharpe": -0.050,
                         "turnover": 0.075, "positive_folds": 25},
    "tsm_deseamed": {"oos_sharpe": 0.680, "bear_sharpe": 0.811,
                     "turnover": 0.067, "positive_folds": 25},
    "carry_normalized_basis": {"oos_sharpe": 0.010, "bear_sharpe": -0.288,
                               "turnover": 0.211, "positive_folds": 23},
    "carry_realized_rollyield": {"oos_sharpe": 0.523, "bear_sharpe": 0.907,
                                 "turnover": 0.031, "positive_folds": 28},
    "blend_tsm_carry_50_50": {"oos_sharpe": 0.463, "bear_sharpe": 0.427,
                              "turnover": 0.131, "positive_folds": 30},
}


def permuted_roll_yield(fut, spot, seams, window, rng, cap=0.35):
    """Realized roll yield with seam gaps permuted across seam dates.

    Placebo building block: the excess gaps at a contract's detected
    seam dates are randomly permuted across those dates only, then the
    standard realized-roll-yield construction (negative trailing
    ``window``-day sum of seam excess gaps, lagged 1 day) is applied.
    Preserves the seam calendar and the per-contract gap-magnitude
    distribution; destroys the timing relationship between accumulated
    roll yield and subsequent returns. With an identity permutation the
    output equals ``futures.realized_roll_yield`` exactly.
    """
    r_fut = fut.pct_change()
    r_spot = spot.reindex(fut.index).ffill().pct_change()
    excess = r_fut - r_spot
    seam_mask = pd.Series(False, index=fut.index)
    seam_idx = pd.DatetimeIndex(seams)
    seam_mask.loc[seam_mask.index.intersection(seam_idx)] = True
    seam_vals = excess[seam_mask]
    if len(seam_vals) > 1:
        perm = rng.permutation(seam_vals.to_numpy())
    else:
        perm = seam_vals.to_numpy()
    permuted_excess = excess.copy()
    permuted_excess.loc[seam_mask] = perm
    seam_excess = permuted_excess.where(seam_mask, 0.0)
    rroll = -seam_excess.rolling(window, min_periods=1).sum().shift(1)
    return rroll.clip(-cap, cap)


def permuted_carry_panel(fut_close, spot_close, seams, window, rng):
    """Panel of permuted realized-roll-yield signals (placebo)."""
    out = pd.DataFrame(index=fut_close.index, columns=fut_close.columns,
                       dtype=float)
    for col in fut_close.columns:
        out[col] = permuted_roll_yield(
            fut_close[col], spot_close[col], seams[col], window, rng
        )
    return out


def build_rroll(fut_close, spot_close, seams, window):
    """Panel of realized-roll-yield signals at a given window."""
    out = pd.DataFrame(index=fut_close.index, columns=fut_close.columns,
                       dtype=float)
    for col in fut_close.columns:
        out[col] = futures.realized_roll_yield(
            fut_close[col], spot_close[col], seams[col], window=window
        )
    return out


def carry_specific_placebo(de_index, fut_close, spot_close, seams,
                           window, n_sim, spy, seed=SEED):
    """Carry-specific placebo null for the realized-roll-yield strategy.

    50 sims of random realized-roll-yield signals (seam-calendar-
    preserving permutation), same rank/inv-vol construction as the
    real strategy. Returns (mean, std) of OOS mean-fold Sharpe.
    """
    rng = np.random.default_rng(seed)
    spy_ret = spy.pct_change().fillna(0.0)
    vol = de_index.pct_change().rolling(63).std().replace(0, np.nan)
    sharps = []
    for _ in range(n_sim):
        sig = permuted_carry_panel(fut_close, spot_close, seams, window, rng)
        w = backtest.carry_weights(sig, vol)
        r = backtest.portfolio_returns_rebalance_clean(
            w, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE,
            rebalance_freq=REBAL
        )
        fm, _ = walk_forward(r, de_index, spy_ret)
        s = [m["sharpe"] for m in fm
             if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
        sharps.append(float(np.mean(s)) if s else 0.0)
    return float(np.mean(sharps)), float(np.std(sharps))


def per_contract_carry(de_index, carry_rroll, spy):
    """Standalone per-contract carry-timing decomposition.

    Mechanism-level test of KMPV carry: for each contract in
    isolation, go long when that contract's own realized roll yield
    is positive (backwardated) and short when negative, inverse-vol
    weighted (symmetric construction, matching the per-contract TSM
    decomposition in E017). Also reports the mean roll-yield level
    (persistent backwardation/contango) and the signal-vs-forward-
    return correlation (predictive content at the contract level).
    """
    spy_ret = spy.pct_change().fillna(0.0)
    splits = backtest.walk_forward_splits(len(de_index), TRAIN, TEST, STEP)
    out = {}
    for col in de_index.columns:
        sig = carry_rroll[[col]]
        rets = de_index[[col]].pct_change()
        vol = rets.rolling(63).std().replace(0, np.nan)
        pos = np.sign(sig).fillna(0.0)
        w = (pos * (1.0 / vol)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
        s = w.abs().sum(axis=1).replace(0, np.nan)
        w = w.div(s, axis=0).fillna(0.0)
        r = backtest.portfolio_returns_rebalance_clean(
            w, de_index[[col]], de_index[[col]],
            tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
        )
        sh = [backtest.metrics(r.loc[r.index.intersection(de_index.index[c:d])]["net"])["sharpe"]
              for (_, _, c, d) in splits]
        sh = [x for x in sh if x == x]
        # Economic-plausibility diagnostics.
        sig_s = carry_rroll[col]
        mean_level = float(sig_s.mean()) if len(sig_s.dropna()) else float("nan")
        fwd = de_index[col].pct_change().shift(-1)
        common = sig_s.dropna().index.intersection(fwd.dropna().index)
        pred_corr = (float(sig_s.loc[common].corr(fwd.loc[common]))
                     if len(common) > 10 else float("nan"))
        out[col] = {
            "oos_sharpe": float(np.mean(sh)) if sh else float("nan"),
            "positive_folds": int(sum(1 for x in sh if x > 0)),
            "n_folds": len(sh),
            "mean_roll_yield": mean_level,
            "signal_fwd_return_corr": pred_corr,
        }
    return out


def tsm_lookback_grid(de_index, spy, placebo_mean, placebo_std):
    """TSM lookback grid {6,9,12,18}m with blended-placebo z-scores."""
    spy_ret = spy.pct_change().fillna(0.0)
    out = {}
    for lb in TSM_LOOKBACK_GRID:
        sig = strategies.time_series_momentum_pure(de_index, lookback=lb, skip=1)
        w = backtest.time_series_momentum_weights(
            sig, de_index, long_only=False, vol_window=63
        )
        res, _ = evaluate(de_index, de_index, spy, w, f"tsm_deseamed_{lb}m")
        z = ((res["oos_sharpe"] - placebo_mean) / placebo_std
             if placebo_std and placebo_std > 0 else float("nan"))
        res["placebo_z"] = float(z)
        res["placebo_mean"] = placebo_mean
        res["placebo_std"] = placebo_std
        out[f"{lb}m"] = res
    return out


def blend_grid(w_tsm, w_carry, de_index, spy, bar):
    """Conditional TSM+carry blend-weight grid (pre-registered)."""
    out = {}
    for tsm_w in BLEND_TSM_WEIGHTS:
        w = tsm_w * w_tsm + (1.0 - tsm_w) * w_carry
        res, _ = evaluate(de_index, de_index, spy, w,
                          f"blend_tsm_carry_tsm{tsm_w:.1f}")
        res["beats_pure_tsm"] = bool(res["oos_sharpe"] > bar)
        out[f"tsm_weight_{tsm_w:.1f}"] = res
    return out


def carry_gate_check(res, z):
    """Pre-registered carry gate evaluation."""
    checks = {
        "oos_sharpe_gte_0.5": bool(res["oos_sharpe"] >= CARRY_GATES["oos_sharpe_gte_0.5"]),
        "carry_placebo_z_gte_3": bool(z >= CARRY_GATES["carry_placebo_z_gte_3"]),
        "bear_sharpe_positive": bool(res["regime_analysis"]["bear"]["sharpe_mean"] > CARRY_GATES["bear_sharpe_positive"]),
        "abs_beta_lte_0.2": bool(abs(res["equity_beta"]) <= CARRY_GATES["abs_beta_lte_0.2"]),
        "turnover_lte_0.05": bool(res["turnover"] <= CARRY_GATES["turnover_lte_0.05"]),
    }
    checks["all_passed"] = all(v for k, v in checks.items() if k != "all_passed")
    return checks


def tsm_gate_check(res):
    """Pre-registered TSM-18m gate evaluation (E017 bar)."""
    checks = {
        "oos_sharpe_gte_1.0": bool(res["oos_sharpe"] >= TSM_GATES["oos_sharpe_gte_1.0"]),
        "placebo_z_gte_3": bool(res.get("placebo_z", 0) >= TSM_GATES["placebo_z_gte_3"]),
        "bear_sharpe_positive": bool(res["regime_analysis"]["bear"]["sharpe_mean"] > TSM_GATES["bear_sharpe_positive"]),
        "abs_beta_lte_0.2": bool(abs(res["equity_beta"]) <= TSM_GATES["abs_beta_lte_0.2"]),
    }
    checks["all_passed"] = all(v for k, v in checks.items() if k != "all_passed")
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-sim", type=int, default=PLACEBO_N_SIM,
                        help="placebo simulations (default 50)")
    args = parser.parse_args()
    n_sim = args.n_sim

    print("=" * 72)
    print("E018: Realized-Roll-Yield Carry Validation + 18m TSM Confirmatory Run")
    print("=" * 72)

    panels = build_panels(FUTURES_UNIVERSE)
    fut_close = panels["fut_close"]
    spot_close = panels["spot_close"]
    de_index = panels["de_index"]
    carry_rroll_252 = panels["carry_rroll"]  # primary window (252d)
    spy = panels["spy"]
    seams_dt = {k: pd.DatetimeIndex(v) for k, v in panels["seams"].items()}

    print(f"\nLoaded: {len(de_index)} common trading days, "
          f"{de_index.shape[1]} futures contracts")
    print(f"  Period: {de_index.index[0].date()} to {de_index.index[-1].date()}")
    print(f"  Pre-registered primary roll-yield window: {PRIMARY_WINDOW}d")
    print(f"  Pre-registered confirmatory TSM lookback: {TSM_CONFIRMATORY_LOOKBACK}m")

    # ---- Part 0: E017 replication anchor (9m grid) ----
    print("\n" + "-" * 72)
    print("Part 0: E017 replication anchor (9m strategy grid)")
    print("-" * 72)
    results_9m = strategy_grid(panels, 9)
    rep_check = {}
    for lbl, recorded in E017_RECORDED.items():
        res = results_9m[lbl]
        bear = res["regime_analysis"]["bear"]["sharpe_mean"]
        rep_check[lbl] = {
            "oos_sharpe": res["oos_sharpe"],
            "oos_sharpe_e017": recorded["oos_sharpe"],
            "bear_sharpe": bear,
            "bear_sharpe_e017": recorded["bear_sharpe"],
            "turnover": res["turnover"],
            "turnover_e017": recorded["turnover"],
            "positive_folds": res["positive_folds"],
            "positive_folds_e017": recorded["positive_folds"],
            "oos_sharpe_delta": res["oos_sharpe"] - recorded["oos_sharpe"],
        }
        ok = abs(res["oos_sharpe"] - recorded["oos_sharpe"]) < 5e-4
        print(f"  {lbl:<28} OOS={res['oos_sharpe']:.3f} "
              f"(E017 {recorded['oos_sharpe']:.3f})  "
              f"bear={bear:+.3f}  turn={res['turnover']:.4f}  "
              f"pos={res['positive_folds']}/{res['n_folds']}  "
              f"{'REPLICATED' if ok else 'DIFFERS'}")

    # ---- Part 1: carry-specific placebo null (primary 252d window) ----
    print("\n" + "-" * 72)
    print(f"Part 1: Carry-specific placebo null "
          f"({n_sim} sims, seam-calendar-preserving permutation, {PRIMARY_WINDOW}d)")
    print("-" * 72)
    # Sanity: identity permutation must reproduce the real signal exactly.
    # Rebuild the realized roll yield with the gaps in their original
    # order (no permutation) and compare to futures.realized_roll_yield.
    identity = pd.DataFrame(index=fut_close.index,
                            columns=fut_close.columns, dtype=float)
    for col in fut_close.columns:
        r_fut = fut_close[col].pct_change()
        r_spot = spot_close[col].reindex(fut_close.index).ffill().pct_change()
        excess = r_fut - r_spot
        seam_mask = pd.Series(False, index=fut_close.index)
        seam_mask.loc[seam_mask.index.intersection(seams_dt[col])] = True
        seam_excess = excess.where(seam_mask, 0.0)
        identity[col] = (-seam_excess.rolling(PRIMARY_WINDOW, min_periods=1)
                       .sum().shift(1).clip(-0.35, 0.35))
    max_diff = 0.0
    for col in fut_close.columns:
        d = np.nanmax(np.abs(identity[col] - carry_rroll_252[col]))
        max_diff = max(max_diff, float(d))
    print(f"  Identity-permutation check: max |permuted(0) - realized_roll_yield| "
          f"= {max_diff:.2e} ({'PASS' if max_diff < 1e-12 else 'FAIL'})")

    # Placebo validity: a random permutation preserves each contract's
    # seam-gap multiset (magnitudes and count) and the seam calendar.
    rng_val = np.random.default_rng(SEED + 1)
    perm_ok = True
    for col in fut_close.columns:
        r_fut = fut_close[col].pct_change()
        r_spot = spot_close[col].reindex(fut_close.index).ffill().pct_change()
        excess = r_fut - r_spot
        seam_mask = pd.Series(False, index=fut_close.index)
        seam_mask.loc[seam_mask.index.intersection(seams_dt[col])] = True
        orig = excess[seam_mask].to_numpy()
        perm = rng_val.permutation(orig)
        if len(orig) > 1 and not np.allclose(np.sort(orig), np.sort(perm)):
            perm_ok = False
            break
    print(f"  Permutation-preserves-gaps check: "
          f"{'PASS' if perm_ok else 'FAIL'}")

    pm_carry, ps_carry = carry_specific_placebo(
        de_index, fut_close, spot_close, seams_dt, PRIMARY_WINDOW, n_sim, spy)
    print(f"  Carry placebo: mean Sharpe={pm_carry:.3f}  std={ps_carry:.3f}  "
          f"n_sim={n_sim}")

    # ---- Part 2: carry gate (primary 252d) ----
    print("\n" + "-" * 72)
    print("Part 2: Pre-registered carry gate (realized roll yield, 252d)")
    print("-" * 72)
    carry_res = results_9m["carry_realized_rollyield"]
    z_carry = (carry_res["oos_sharpe"] - pm_carry) / ps_carry if ps_carry > 0 else float("nan")
    carry_res["carry_placebo_z"] = float(z_carry)
    carry_res["carry_placebo_mean"] = pm_carry
    carry_res["carry_placebo_std"] = ps_carry
    carry_gates = carry_gate_check(carry_res, z_carry)
    print(f"  carry_realized_rollyield  OOS_Sharpe={carry_res['oos_sharpe']:.3f}  "
          f"carry_z={z_carry:.2f}  beta={carry_res['equity_beta']:+.3f}  "
          f"bear={carry_res['regime_analysis']['bear']['sharpe_mean']:+.3f}  "
          f"turn={carry_res['turnover']:.4f}")
    for g, ok in carry_gates.items():
        print(f"    {g:<28} {'PASS' if ok else 'FAIL'}")

    # ---- Part 3: roll-yield window sensitivity {126, 252, 504} ----
    print("\n" + "-" * 72)
    print("Part 3: Roll-yield window sensitivity {126, 252, 504} days")
    print("-" * 72)
    window_results = {}
    for win in WINDOWS:
        if win == PRIMARY_WINDOW:
            rroll_w = carry_rroll_252
            pm_w, ps_w = pm_carry, ps_carry
        else:
            rroll_w = build_rroll(fut_close, spot_close, seams_dt, win)
            pm_w, ps_w = carry_specific_placebo(
                de_index, fut_close, spot_close, seams_dt, win, n_sim, spy,
                seed=SEED + win)
        res, _ = evaluate(de_index, de_index, spy,
                          backtest.carry_weights(rroll_w, de_index.pct_change()
                                               .rolling(63).std().replace(0, np.nan)),
                          f"carry_rroll_{win}d")
        z_w = (res["oos_sharpe"] - pm_w) / ps_w if ps_w > 0 else float("nan")
        res["carry_placebo_z"] = float(z_w)
        res["carry_placebo_mean"] = pm_w
        res["carry_placebo_std"] = ps_w
        res["window_days"] = win
        res["is_primary"] = bool(win == PRIMARY_WINDOW)
        res["gates"] = carry_gate_check(res, z_w)
        window_results[f"{win}d"] = res
        print(f"  window {win:<4} OOS_Sharpe={res['oos_sharpe']:.3f}  "
              f"carry_z={z_w:.2f}  beta={res['equity_beta']:+.3f}  "
              f"bear={res['regime_analysis']['bear']['sharpe_mean']:+.3f}  "
              f"turn={res['turnover']:.4f}  "
              f"gates={'PASS' if res['gates']['all_passed'] else 'FAIL'}")

    # ---- Part 4: per-contract carry decomposition ----
    print("\n" + "-" * 72)
    print("Part 4: Per-contract carry decomposition (standalone carry timing, 252d)")
    print("-" * 72)
    per_contract = per_contract_carry(de_index, carry_rroll_252, spy)
    print(f"  {'ctr':<6} {'OOS Sharpe':>10} {'pos folds':>9} "
          f"{'mean rroll':>10} {'sig/fwd corr':>12}")
    for col, v in per_contract.items():
        print(f"  {col:<6} {v['oos_sharpe']:>+10.3f} "
              f"{v['positive_folds']:>5}/{v['n_folds']:<3} "
              f"{v['mean_roll_yield']:>+10.4f} "
              f"{v['signal_fwd_return_corr']:>+12.3f}")

    # ---- Part 5: blended placebo + TSM 18m confirmatory run ----
    print("\n" + "-" * 72)
    print("Part 5: TSM lookback grid + pre-registered 18m confirmatory run")
    print("-" * 72)
    print(f"  Blended placebo null ({n_sim} random TSM + random carry, 50/50)...")
    pm_blend, ps_blend = blended_placebo(de_index, spy, n_sim=n_sim)
    print(f"    Placebo: mean Sharpe={pm_blend:.3f}  std={ps_blend:.3f}  "
          f"n_sim={n_sim}")
    lookbacks = tsm_lookback_grid(de_index, spy, pm_blend, ps_blend)
    for lb, res in lookbacks.items():
        marker = " <- CONFIRMATORY (pre-registered)" if lb == f"{TSM_CONFIRMATORY_LOOKBACK}m" \
            else (" <- registered primary (E017)" if lb == "9m" else "")
        print(f"  tsm_deseamed_{lb:<4} OOS_Sharpe={res['oos_sharpe']:.3f}  "
              f"z={res['placebo_z']:.2f}  beta={res['equity_beta']:+.3f}  "
              f"bear={res['regime_analysis']['bear']['sharpe_mean']:+.3f}  "
              f"turn={res['turnover']:.4f}  pos={res['positive_folds']}/{res['n_folds']}"
              f"{marker}")
    tsm18 = lookbacks[f"{TSM_CONFIRMATORY_LOOKBACK}m"]
    tsm18_gates = tsm_gate_check(tsm18)
    print(f"\n  Pre-registered TSM-{TSM_CONFIRMATORY_LOOKBACK}m gates (E017 bar):")
    for g, ok in tsm18_gates.items():
        print(f"    {g:<28} {'PASS' if ok else 'FAIL'}")
    tsm9 = lookbacks["9m"]
    print(f"  Registered primary (9m) OOS Sharpe={tsm9['oos_sharpe']:.3f} "
          f"(E017 reported 0.680) - remains the registered result.")

    # ---- Part 6: conditional blend grid ----
    blend_results = None
    if carry_gates["all_passed"]:
        print("\n" + "-" * 72)
        print("Part 6: TSM+carry blend-weight grid (carry cleared its gates)")
        print("-" * 72)
        vol = de_index.pct_change().rolling(63).std().replace(0, np.nan)
        w_tsm9 = backtest.time_series_momentum_weights(
            strategies.time_series_momentum_pure(de_index, lookback=9, skip=1),
            de_index, long_only=False, vol_window=63)
        w_carry252 = backtest.carry_weights(carry_rroll_252, vol)
        blend_results = blend_grid(w_tsm9, w_carry252, de_index, spy,
                                 BLEND_FALSIFICATION_BAR)
        for name, res in blend_results.items():
            z_b = ((res["oos_sharpe"] - pm_blend) / ps_blend
                   if ps_blend and ps_blend > 0 else float("nan"))
            res["placebo_z"] = float(z_b)
            res["placebo_mean"] = pm_blend
            res["placebo_std"] = ps_blend
            print(f"  {name:<28} OOS_Sharpe={res['oos_sharpe']:.3f}  "
                  f"z={res['placebo_z']:.2f}  "
                  f"beta={res['equity_beta']:+.3f}  "
                  f"bear={res['regime_analysis']['bear']['sharpe_mean']:+.3f}  "
                  f"turn={res['turnover']:.4f}  "
                  f"beats_pure_tsm={res['beats_pure_tsm']}")
        any_beat = any(res["beats_pure_tsm"] for res in blend_results.values())
        print(f"  Falsification (>=1 blend beats pure TSM-9m {BLEND_FALSIFICATION_BAR:.3f}): "
              f"{'YES' if any_beat else 'NO - carry adds nothing to the book'}")
    else:
        print("\n  Part 6: blend grid SKIPPED (carry did not clear its pre-registered gates)")

    # Signal complementarity diagnostics.
    tsm_sig = strategies.time_series_momentum_pure(de_index, lookback=9, skip=1)
    sig_corr = float(tsm_sig.stack().corr(carry_rroll_252.stack()))
    print(f"\n  Signal correlation TSM(9m) vs realized-roll-yield carry(252d): {sig_corr:.3f}")

    # ---- Summary ----
    print("\n" + "=" * 72)
    print("E018 Summary")
    print("=" * 72)
    print(f"  E017 replication: 9m grid reproduced to <5e-4: "
          f"{all(abs(v['oos_sharpe_delta']) < 5e-4 for v in rep_check.values())}")
    print(f"  Carry (252d): OOS Sharpe={carry_res['oos_sharpe']:.3f}, "
          f"carry-specific z={z_carry:.2f} "
          f"(placebo {pm_carry:.3f} +/- {ps_carry:.3f})")
    print(f"  Carry gates: {'ALL PASSED' if carry_gates['all_passed'] else 'NOT all passed'}")
    print(f"  Window sensitivity: "
          + ", ".join(f"{w}d={window_results[f'{w}d']['oos_sharpe']:.3f}" for w in WINDOWS))
    print(f"  TSM-18m confirmatory: OOS Sharpe={tsm18['oos_sharpe']:.3f}, "
          f"z={tsm18['placebo_z']:.2f}, gates "
          f"{'ALL PASSED' if tsm18_gates['all_passed'] else 'NOT all passed'}")
    print(f"  Registered TSM primary remains 9m ({tsm9['oos_sharpe']:.3f})")
    if blend_results is not None:
        print(f"  Blend grid: best={max(r['oos_sharpe'] for r in blend_results.values()):.3f} "
              f"(falsification bar {BLEND_FALSIFICATION_BAR:.3f})")

    # ---- Save ----
    result = {
        "experiment": "E018",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "description": ("Validation of realized-roll-yield carry as a standalone "
                        "cross-asset component (carry-specific placebo, window "
                        "sensitivity, per-contract decomposition) plus a "
                        "pre-registered confirmatory run of 18m TSM."),
        "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP},
        "rebalance_freq_days": REBAL,
        "pre_registered": {
            "primary_roll_yield_window_days": PRIMARY_WINDOW,
            "primary_window_justification": "252d unchanged from E016/E017; 126/504d are sensitivity only",
            "carry_gates": {k: v for k, v in CARRY_GATES.items()},
            "carry_placebo_construction": ("50 sims; per contract, detected seam excess gaps "
                                           "randomly permuted across that contract's seam dates only "
                                           "(preserves seam calendar + gap-magnitude distribution); "
                                           "same trailing-window realized-roll-yield construction, "
                                           "same dollar-neutral top/bottom-half inv-vol weights"),
            "tsm_confirmatory_lookback_months": TSM_CONFIRMATORY_LOOKBACK,
            "tsm_confirmatory_justification": ("only lookback top-2 on BOTH samples "
                                               "(E016 short 0.894, E017 extended 0.805); "
                                               "selected from two-sample evidence, not by "
                                               "maximizing extended-sample Sharpe"),
            "tsm_gates": {k: v for k, v in TSM_GATES.items()},
            "registered_tsm_primary": "9m (E017); 18m is a confirmatory run, goalposts not moved",
            "blend_grid": {"tsm_weights": BLEND_TSM_WEIGHTS,
                           "conditional_on": "carry clearing all pre-registered gates",
                           "falsification_bar": BLEND_FALSIFICATION_BAR},
            "multiple_testing_notes": ("3 windows x 50-sim placebo; 4 lookbacks reported; "
                                       "primary window/lookback fixed ex-ante"),
        },
        "universe": {
            "futures": list(FUTURES_UNIVERSE.keys()),
            "pairs": {k: v[0] for k, v in FUTURES_UNIVERSE.items()},
            "n_days": int(len(de_index)),
            "start": str(de_index.index[0].date()),
            "end": str(de_index.index[-1].date()),
        },
        "e017_replication": rep_check,
        "carry_specific_placebo": {"mean": pm_carry, "std": ps_carry,
                                   "n_sim": n_sim,
                                   "identity_permutation_max_diff": max_diff},
        "carry_gates": carry_gates,
        "carry_primary_result": carry_res,
        "window_sensitivity": window_results,
        "per_contract_carry": per_contract,
        "blended_placebo": {"mean": pm_blend, "std": ps_blend, "n_sim": n_sim,
                            "type": "random TSM + random carry, 50/50 blend"},
        "tsm_lookback_grid": lookbacks,
        "tsm18m_gates": tsm18_gates,
        "blend_grid": blend_results,
        "tsm_carry_signal_correlation": sig_corr,
    }

    out_path = os.path.join("experiments", "e018_carry_validation.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
