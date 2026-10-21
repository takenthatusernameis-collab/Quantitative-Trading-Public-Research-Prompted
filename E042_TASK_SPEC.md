# E042 Task Specification (for next agent)

**Date**: 2026-10-12
**Status**: Ready to execute
**Estimated time**: ~15-25 minutes (single confirmatory run + placebo, no sensitivity grid)
**Depends on**: E041 (`experiments/e041_market_neutral_portfolio.json`,
`experiments/e041_sensitivity_grid.json`, `src/portfolio_opt.py`)

## Background

E041 (just completed) tested whether a walk-forward optimized blend of
the five validated components can form a market-neutral total portfolio
(|β vs SPY| ≤ 0.1) with OOS Sharpe ≥ 0.8 (c2c). The pre-registered
**max_sharpe** blend was **REJECTED (3/5 gates)**:

- G1 OOS Sharpe 0.981 (PASS), G4 bear +0.850 (PASS), G5 turnover
  0.0088 (PASS).
- **G3 market-neutrality FAIL**: realized β +0.173 full-sample /
  +0.157 OOS vs the 0.10 bar.
- **G2 placebo z -1.29 (FAIL)**; **FE2 falsified** (in-sample Sharpe
  edge -0.289 — the β-constraint costs more Sharpe than max_sharpe
  optimization adds).

Two material findings recorded:
1. **The DN low-beta component is NOT market-neutral under the c2c
   convention** (β +1.02; the recorded -0.035 was the *overnight* β
   under which E012/E013 validated it). `dollar_neutral_longshort_weights`
   sizes the k largest rank-percentiles long, which under
   `rank(ascending=False)` is the smallest-signal (highest-β) names —
   the reverse of its docstring and of the low-beta intent. Used as-is
   (pre-registered component spec); recorded as established context.
2. **Market-neutrality and Sharpe maximization conflict** on this
   universe (the highest-Sharpe component, TSM pure OOS 1.806, carries
   β +0.856).

**The key lead**: the E041 sensitivity grid (96 pre-registered configs,
reported NOT gated) showed that a **min_variance** blend at a tighter β
cap (0.05) achieves market-neutrality (β +0.094) with OOS Sharpe 0.979
and bear Sharpe +1.967 — passing G1/G3/G4/G5 — while the max_sharpe
objective cannot. This is principled (DeMiguel et al. 2009:
minimum-variance is the most robust objective out-of-sample precisely
because it does not chase noisy mean/β estimates) but was found by
searching 96 configs, so it is multiple-testing-contaminated and MUST be
pre-registered before running.

## Pre-registration (fix before running; goalposts not moved)

**Primary configuration**:
- Objective: **min_variance** (`portfolio_opt.optimize_portfolio_weights`
  with `method="min_var"`).
- Beta constraint: **0.05** vs SPY AND vs the equal-weight de-seamed
  futures index. Justify the 0.05 cap from the E041 grid evidence (the
  max_sharpe β≤0.10 cap did not hold OOS; 0.05 is the tightest cap at
  which min_variance cleared G1+G3 in the grid) — NOT by maximizing the
  grid OOS Sharpe.
- Walk-forward 504/21/63, c2c, class-appropriate base costs
  (equity/macro 0.5+0.2bps, futures 1.0+0.5bps), all 5 components,
  SEED=42, warm-up 252d. Reuse `src/portfolio_opt.py` and
  `experiments/run_e041.py` (the `sensitivity_grid`/`evaluate_blend`
  machinery already supports `method="min_var"`).

**Promotion gates (identical bars to E041)**:
- G1: OOS Sharpe (c2c) ≥ 0.8.
- G2: placebo z ≥ 3.0, **50 sims, component-permutation null MATCHED to
  the constraint** — for min_variance, re-draw Dirichlet(1) weights
  *projected onto the β ≤ 0.05 cap* (e.g. via the same linprog
  feasibility phase), so the placebo is not biased against the constraint
  (E041's unconstrained-Dirichlet placebo is recorded as a caveat: its
  negative z measures the constraint's Sharpe cost, not a lack of edge).
- G3: |β vs SPY| ≤ 0.1 — report BOTH full-sample and OOS.
- G4: bear-market Sharpe (SPY fold < -5%) > 0.
- G5: daily turnover ≤ 0.15.

**Falsification expectations**:
- FE1: ≥ 80% of component pairs with |corr| ≤ 0.5 (already satisfied,
  E041 FE1 = 10/10).
- FE2: re-define for min_variance — min_variance is expected to have
  LOWER in-sample Sharpe than 1/N by construction, so use out-of-sample
  variance reduction vs 1/N (or drop FE2 as not-applicable and record
  why). Do NOT reuse E041's in-sample-Sharpe-edge FE2 for min_variance.

**Robustness (reported, not gated)**:
- Cost sweep {0, base, 10+5, 20+5} bps.
- Component-set ablation: all-5 vs macro-inclusive-3 (the equity sleeves
  are the c2c-β source).
- Split-half stability of the min-variance weights (the E041 max_sharpe
  solution was non-monotonic in the β cap, so verify min_variance is
  stable).
- β-constrained placebo (G2) AND, as a diagnostic, the unconstrained
  Dirichlet placebo (to show the constraint's Sharpe cost).

**Decision rule**: promote to STRATEGIES + README only if ALL five gates
pass on the pre-registered primary config with the β-constrained placebo;
otherwise record as REJECTED and close the market-neutral-total-portfolio
line (the surviving edges remain the component strategies per the E040
close-out).

## Constraints

- Do NOT modify the validated component constructions
  (`src/backtest.py`, `src/strategies.py`, `src/futures.py`,
  `src/macro.py`); build on `src/portfolio_opt.py`.
- Keep `SEED=42`; close-to-close primary convention (v1.2.3).
- Record the dn_lowbeta c2c-β finding (E041 `convention_findings`) as
  established context; do not re-litigate it.
- Multiple-testing discipline: the 0.05 cap and min_variance objective
  are pre-registered from the E041 grid evidence on PRINCIPLED grounds
  (variance-minimization robustness + the tightest market-neutral cap),
  not by maximizing the grid OOS Sharpe. If the primary fails, do NOT
  search the grid again for a passing config — record the negative and
  close the line.

## Completion criteria

1. `experiments/run_e042.py` driver (reuse `run_e041.py` structure).
2. `experiments/e042_minvar_market_neutral.json` with the full gate
   table, β-constrained placebo, cost sweep, ablation, stability check.
3. Ledger entry (RESEARCH_LEDGER.md) with the gate table, decision, and
   the FE2 re-definition for min_variance.
4. If promoted: add to STRATEGIES (README.md) and bump PRIORITIZATION.md
   to v1.2.6. If rejected: record the negative and state that the
   market-neutral-total-portfolio line is closed.
