# Durable Handoff — Next Agentic Session

**Timestamp:** 2026-10-30T16-24-11Z
**Branch:** `main` (up to date with `origin/main`)
**Working tree:** clean except `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/` `.pyc` files (compiled artifacts, not source). No uncommitted source changes.
**Last commits:** `3da5278`, `d3d5d11`, `08166c8`, `9cccf68` (all `chore(kilo): checkpoint agent session`).

## Initial task message (this handoff)

> **Task: Replace the SLSQP tangency-QP solves in `src/portfolio_opt.py` with a well-conditioned deterministic solver (exact active-set enumeration of all KKT points for N ≤ 5), then deliberately re-pin the affected artifacts. Do NOT re-pin to silence drift without the solver change. No research conclusion may change.**

## Repository state

Research phase complete (E001–E049). Five validated components: equity TSM flagship, DN low-beta sort, futures TSM 18m, futures realized-roll-yield carry, macro momentum. The market-neutral-total-portfolio line is **CLOSED** (E042 PARTIAL 4/5, G2 fails; E042b REJECTED 4/5, G2 fails) — no blend of the validated components is simultaneously market-neutral and placebo-significant on free public data.

`src/portfolio_opt.py` was already fixed once (E049): the `max_sharpe` tangency branch and `project_onto_beta_cap` now judge the solver answer on the **problem's constraints** (new `_tangency_feasible`), never on `res.success`. `tests/test_portfolio_opt.py` (5 tests) is a first-class step of `scripts/check.sh`; it fails on pre-fix code and passes after. One golden was deliberately re-pinned via `scripts/check_golden_baseline.py --update` (E042 lead `/placebo_constrained` block; 5 numeric, 0 structural diffs; decision unchanged). The primary (quick) verification gate is green again.

## Why this is the task (the open item)

The exit-status dependence was removed, but the tangency QP is **still ill-conditioned**:
- `min_var` answers move by up to ~2.6e-05 in daily weights at the 1-ulp level.
- A 1e-14 covariance perturbation still moves the E042-lead OOS Sharpe by ~3e-02.
- Residual drift vs the committed goldens: E041 portfolio **133** numeric, E041 grid **29**, E042-primary **56**, E042 grid **42** differences.

The fix is a *research-engineering* decision, not a mechanical repair: replace the SLSQP QP solves with a well-conditioned, deterministic solver. For N ≤ 5 an exact active-set enumeration of all KKT points is feasible and was already used in-session as the reference oracle (it reproduced the committed golden's `/primary` block to 5e-9). Then deliberately re-pin the affected artifacts so the replacement is visible in the diff.

## Second defect — deliberately NOT fixed (follow-on)

`y0 = w_feas / max(mu_s'w_feas, 1e-12)` at `src/portfolio_opt.py:253` masks a negative denominator; at the 2019-10-16 rebalance the initial point has magnitude 8.1e+11 and violates `mu'y = 1` by 6.4e+09. SLSQP returns garbage there (objective 3.7e+20), which the new feasibility check correctly rejects, so the shipped code falls back to the LP vertex exactly as the golden did. Fixing the start point (a max-`mu_s'w` LP on the feasible simplex) would converge to the exact optimum and **change published numbers** — leave for the same deliberate re-pin decision as the main task.

## E041 residual drift — bounded investigation

E041's three structural differences are resolved (the "8 of 96" count is stable; decision REJECTED 3/5 unchanged). The remaining 133 numeric differences are 1-ulp sensitivity of the ill-conditioned QP; do not re-pin to silence. Investigate only if the solver change does not collapse them.

## Verification commands (run BEFORE declaring done)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
git status --short | grep -v __pycache__
```

## Rules (from AGENTS.md, do not violate)

- Always use `SEED=42`. Never move goalposts, change tolerances/drivers/skips, or change research decisions as a side effect of verification.
- `experiments/*.json` are canonical; `run_all_verification.py` backs up and restores them — never commit verification output. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Replacing an artifact requires deliberate `scripts/check_golden_baseline.py --update` so the replacement is in the diff.
- Offline mode: `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard (cache coverage invariant enforced by `scripts/check_data_coverage.py`).
- Python 3; no separate linter — run `python3 -m py_compile` on changed files.
- CI workflow cannot be created by agents (controller restores `.github/workflows/`, token lacks push permission); template at `.github/workflow-templates/verification-gate.yml`.

## Handoff outcome

Once the deterministic KKT-enumeration solver lands, the primary gate is green, and every re-pin is visible in the diff with no research conclusion changed, the session is done. Items 2 and 3 are its natural follow-ons.
