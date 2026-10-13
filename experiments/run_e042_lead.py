#!/usr/bin/env python3
"""E042 Lead-Config Confirmatory Validation.

The E042 sensitivity grid (sensitivity_market_neutral_summary) flags 8
configs that are market-neutral (|equity_beta| <= 0.1) AND survive the
G1 c2c Sharpe gate (>= 0.8). The grid only reports OOS Sharpe / beta /
turnover / bear Sharpe, however - it does NOT run the G2 beta-constrained
placebo-significance gate, which is run only for the primary min_var config
(z = 1.95, FAIL). The grid therefore marks them "NOT promoted - requires
confirmatory run."

This script runs the FULL v1.2.3 promotion gate set (G1-G5) plus the FE1/FE2
falsifications on the strongest documented lead:

    max_sharpe, beta <= 0.1, rebalance 63d, macro_inclusive_3
    (grid OOS Sharpe = 0.866, grid equity_beta = -0.001)

It reuses experiments/run_e042.py's exact component builders, blend
evaluator and walk-forward cadence, and the G2 beta-constrained placebo
null (50 sims, SEED=42) projected through the lead config's component subset
and beta cap - a matched null that preserves the rebalance/execution
structure while destroying timing content.

Output: experiments/e042_lead_config_confirmatory.json

Reproduction:  SEED=42 python3 experiments/run_e042_lead.py
"""

import json
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = os.path.join(ROOT, "experiments")
sys.path.insert(0, ROOT)
sys.path.insert(0, EXP)

from src import portfolio_opt
import run_e042 as R

LEAD = {
    "name": "max_sharpe_beta0.1_63d_macro_inclusive_3",
    "method": "max_sharpe",
    "beta_constraint": 0.1,
    "rebalance_freq": 63,
    "component_set": "macro_inclusive_3",
    "grid_oos_sharpe": 0.866,
    "grid_equity_beta": -0.001,
    "source": "E042 sensitivity_grid (e042_sensitivity_grid.json)",
}


def _benchmarks(cols, comp):
    sub_bench = comp["spy_ret"] if any(
        c in ("tsm_pure", "dn_lowbeta", "macro_momentum") for c in cols) else None
    sub_fb = comp["fut_index_ret"] if any(
        c in ("futures_tsm", "futures_carry") for c in cols) else None
    return sub_bench, sub_fb


def lead_weights(component_returns, comp):
    cols = R.SENS_SETS[LEAD["component_set"]]
    sub = component_returns[cols]
    sub_bench, sub_fb = _benchmarks(cols, comp)
    W = portfolio_opt.walk_forward_blend_weights(
        sub, benchmark_returns=sub_bench,
        futures_benchmark_returns=sub_fb,
        formation_window=R.FORMATION, rebalance_freq=LEAD["rebalance_freq"],
        beta_constraint=LEAD["beta_constraint"], method=LEAD["method"],
        seed=R.SEED, n_grid=0)
    gross, turnover, net = R.blend_series(sub, W, R.TC_EQUITY, R.SL_EQUITY)
    primary = R.evaluate_blend(net, sub.index, comp["spy_ret"],
                               R.TC_EQUITY, R.SL_EQUITY, W)
    return W, net, primary, sub, cols


def lead_placebo(component_returns, comp, n_sim=R.PLACEBO_N):
    cols = R.SENS_SETS[LEAD["component_set"]]
    sub = component_returns[cols]
    sub_bench, sub_fb = _benchmarks(cols, comp)
    idx = sub.index
    rng = np.random.default_rng(R.SEED)
    pl = []
    for _ in range(n_sim):
        pw = portfolio_opt.portfolio_placebo_weights_beta_constrained(
            sub, formation_window=R.FORMATION,
            benchmark_returns=sub_bench,
            futures_benchmark_returns=sub_fb,
            beta_constraint=LEAD["beta_constraint"],
            n_simulations=1, seed=int(rng.integers(1 << 30)),
            rebalance_freq=LEAD["rebalance_freq"])[0]
        _, _, pnet = R.blend_series(sub, pw, R.TC_EQUITY, R.SL_EQUITY)
        folds, _ = R.fold_metrics(pnet, idx, comp["spy_ret"])
        sh = [m["sharpe"] for m in folds
              if m.get("sharpe") is not None
              and not np.isnan(m.get("sharpe", float("nan")))]
        pl.append(float(np.mean(sh)) if sh else 0.0)
    return pl


def gates(primary, placebo_z):
    g = {
        "G1_oos_sharpe_gte_0.8": primary["oos_sharpe"] >= 0.8,
        "G2_placebo_z_gte_3.0": placebo_z >= 3.0,
        "G3_abs_beta_vs_spy_lte_0.1": abs(primary["equity_beta"]) <= 0.1,
        "G4_bear_sharpe_gt_0": primary["bear_sharpe"] > 0,
        "G5_turnover_lte_0.15": primary["turnover"] <= 0.15,
    }
    n = sum(g.values())
    return g, n


def main():
    print("=" * 72)
    print("E042 LEAD-CONFIG CONFIRMATORY VALIDATION")
    print(f"Config: {LEAD['name']}  ({LEAD['method']}, beta<={LEAD['beta_constraint']}, "
          f"{LEAD['rebalance_freq']}d, {LEAD['component_set']})")
    print(f"Source: {LEAD['source']}  (grid OOS={LEAD['grid_oos_sharpe']}, "
          f"beta={LEAD['grid_equity_beta']})")
    print("Method: faithful to run_e042.py primary path + matched G2 placebo "
          "(50 sims, SEED=42)")
    print("=" * 72)
    t0 = time.time()
    comp = R.build_component_returns()
    cr = comp["returns"]
    W, net, primary, sub, cols = lead_weights(cr, comp)
    pl = lead_placebo(cr, comp)
    pm, ps = float(np.mean(pl)), float(np.std(pl))
    cz = (primary["oos_sharpe"] - pm) / ps if ps > 0 else float("nan")
    g, n = gates(primary, cz)
    all_pass = (n == 5)

    fe1 = R.fe1_diversification(sub)
    fe2 = R.fe2_variance_reduction(sub, net, W, sub.index, comp["spy_ret"])

    print(f"\nLead component set ({len(cols)}): {cols}")
    print(f"  OOS Sharpe (c2c)  = {primary['oos_sharpe']:.3f}   "
          f"(std {primary['oos_sharpe_std']:.3f}, "
          f"{primary['positive_folds']}/{primary['n_folds']} +folds)")
    print(f"  Equity beta vs SPY = {primary['equity_beta']:+.4f}  "
          f"(OOS {primary['oos_equity_beta']:+.4f})")
    print(f"  Turnover           = {primary['turnover']:.4f}")
    print(f"  Bear Sharpe        = {primary['bear_sharpe']:+.3f}  "
          f"({primary['bear_folds']} bear folds)")
    print(f"  IS Sharpe / maxDD  = {primary['is_sharpe']:.3f} / "
          f"{primary['max_drawdown']:.3f}")
    print(f"  Mean component wts: " + ", ".join(
        f"{c}={W[c].mean():.3f}" for c in W.columns))

    print(f"\nBeta-constrained placebo null ({R.PLACEBO_N} sims, cap "
          f"<={LEAD['beta_constraint']}, 63d rebalance):")
    print(f"  placebo mean={pm:.3f} std={ps:.3f} "
          f"min={min(pl):.3f} max={max(pl):.3f}")
    print(f"  G2 placebo z = {cz:.2f}  (gate >= 3.0)")

    print("\n" + "-" * 72)
    print("PRE-REGISTERED PROMOTION GATES (v1.2.3)")
    print("-" * 72)
    bars = {"G1_oos_sharpe_gte_0.8": 0.8, "G2_placebo_z_gte_3.0": 3.0,
            "G3_abs_beta_vs_spy_lte_0.1": 0.1, "G4_bear_sharpe_gt_0": 0.0,
            "G5_turnover_lte_0.15": 0.15}
    vals = {"G1_oos_sharpe_gte_0.8": primary["oos_sharpe"],
            "G2_placebo_z_gte_3.0": cz,
            "G3_abs_beta_vs_spy_lte_0.1": abs(primary["equity_beta"]),
            "G4_bear_sharpe_gt_0": primary["bear_sharpe"],
            "G5_turnover_lte_0.15": primary["turnover"]}
    for k in ["G1_oos_sharpe_gte_0.8", "G2_placebo_z_gte_3.0",
              "G3_abs_beta_vs_spy_lte_0.1", "G4_bear_sharpe_gt_0",
              "G5_turnover_lte_0.15"]:
        ok = "PASS" if g[k] else "FAIL"
        print(f"  {k:<32} bar={bars[k]:<5} val={vals[k]:<8.3f} {ok}")
    print(f"  Gates passed: {n}/5")

    print("\nFalsifications:")
    print(f"  FE1 (diversification) passed = {fe1.get('passed')}")
    print(f"  FE2 (OOS var-reduction vs 1/N) passed = "
          f"{fe2.get('passed', False)}")

    decision = "PROMOTED (all gates pass - OVERTURNS E042 closure)" \
        if all_pass else "REJECTED (a gate failed - consistent with E042 closure)"
    print("\n" + "=" * 72)
    print(f"DECISION: {decision}")
    print(f"runtime: {time.time()-t0:.1f}s")
    print("=" * 72)

    out = {
        "experiment": "e042_lead_config_confirmatory",
        "source": "E042 sensitivity grid lead (max_sharpe beta<=0.1 63d "
                  "macro_inclusive_3), validated against the FULL v1.2.3 "
                  "promotion gates including the G2 beta-constrained placebo",
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "seed": R.SEED,
        "config": LEAD,
        "component_set": list(cols),
        "primary": {
            "method": LEAD["method"],
            "beta_constraint": LEAD["beta_constraint"],
            "rebalance_freq": LEAD["rebalance_freq"],
            "n_grid": 0,
            "oos_sharpe": primary["oos_sharpe"],
            "oos_sharpe_std": primary["oos_sharpe_std"],
            "positive_folds": primary["positive_folds"],
            "n_folds": primary["n_folds"],
            "equity_beta": primary["equity_beta"],
            "oos_equity_beta": primary["oos_equity_beta"],
            "turnover": primary["turnover"],
            "bear_sharpe": primary["bear_sharpe"],
            "bear_folds": primary["bear_folds"],
            "is_sharpe": primary["is_sharpe"],
            "max_drawdown": primary["max_drawdown"],
            "regime_analysis": primary["regime_analysis"],
            "mean_component_weights": {c: float(W[c].mean()) for c in W.columns},
        },
        "placebo_constrained": {
            "n_sim": R.PLACEBO_N,
            "mean_sharpe": pm,
            "std_sharpe": ps,
            "min_sharpe": float(min(pl)),
            "max_sharpe": float(max(pl)),
            "z_score": cz,
            "gate": R.GATES["G2_placebo_z_gte_3.0"],
        },
        "gates": g,
        "gates_passed_count": n,
        "gates_total": 5,
        "fe1_diversification": {
            "passed": fe1.get("passed"),
            "n_pairs_pass": fe1.get("n_pairs_pass"),
            "n_pairs": fe1.get("n_pairs"),
        },
        "fe2_variance_reduction": {
            "passed": fe2.get("passed", False),
            "variance_ratio": fe2.get("oos_variance_ratio"),
        },
        "decision": "PROMOTED" if all_pass else "REJECTED",
        "runtime_sec": round(time.time() - t0, 1),
    }
    path = os.path.join(EXP, "e042_lead_config_confirmatory.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {path}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
