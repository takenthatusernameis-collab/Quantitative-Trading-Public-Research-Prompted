# Durable Handoff — Next Agentic Session

**Timestamp:** 2026-10-30T16:24:43Z
**Branch:** `main` (up to date with `origin/main`)
**Working tree:** clean. No uncommitted source changes.
**Last commits:** `465cdf6`, `35112b5`, `fa5e721` (all `chore(kilo): checkpoint agent session`).

## Initial task for next session

Replace the SLSQP QP solves in `src/portfolio_opt.py` with a well-conditioned deterministic solver (for N ≤ 5, exact active-set enumeration of all KKT points is feasible and was used here as the reference oracle), then deliberately re-pin the affected artifacts via `scripts/check_golden_baseline.py --update` (replacement must be visible in diff). Do NOT re-pin to silence drift without the solver change. No research conclusion may change.

## Repository state

Research phase complete (E001–E043). Five validated components: equity TSM flagship, DN low-beta sort, futures TSM 18m, futures realized-roll-yield carry, macro momentum. Market-neutral-total-portfolio line CLOSED (E042 PARTIAL 4/5, E042b REJECTED 4/5).

`src/portfolio_opt.py` fixed (E049): `max_sharpe` tangency branch and `project_onto_beta_cap` now judge solver answer on QP constraints (`_tangency_feasible`), never `res.success`. `tests/test_portfolio_opt.py` added (5 tests, first-class step of `scripts/check.sh`). One golden re-pinned (E042 lead `/placebo_constrained` block; 5 numeric, 0 structural; decision unchanged). Primary gate green.

## Open items (priority order)

1. QP ill-conditioning (highest value): replace SLSQP solves with deterministic solver; re-pin artifacts. Residual drift: E041 portfolio 133, E041 grid 29, E042-primary 56, E042 grid 42 numeric diffs.
2. Second defect (not fixed): `y0 = w_feas / max(mu_s'w_feas, 1e-12)` at `src/portfolio_opt.py:253` masks negative denominator (2019-10-16 rebalance: magnitude 8.1e+11, violates `mu'y=1` by 6.4e+09). Fix would change published numbers — leave for same deliberate re-pin as item 1.
3. E041 residual drift: bounded; investigate only if item 1's solver change does not collapse the 133 numeric diffs.

## Verification commands (run before declaring done)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
git status --short | grep -v __pycache__
```

## Rules (from AGENTS.md)

- Always SEED=42. Never move goalposts, tolerances, drivers, skips, or research decisions as side effect of verification.
- `experiments/*.json` canonical; verification backs up/restores — never commit verification output. Interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Replacing an artifact requires deliberate `scripts/check_golden_baseline.py --update`.
- Offline: `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard.
- Python 3; no linter — `python3 -m py_compile` on changed files.
- CI workflow cannot be created by agents.

## Handoff outcome

Item 1 (deterministic solver + deliberate re-pin) is the clear, bounded, high-value task. Items 2 and 3 are natural follow-ons. Once item 1 lands and primary gate is green with all re-pins visible in diff, session is done.
