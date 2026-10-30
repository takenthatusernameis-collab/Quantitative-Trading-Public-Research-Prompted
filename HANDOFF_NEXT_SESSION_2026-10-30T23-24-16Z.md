# Durable Handoff — Next Agentic Session

**Timestamp:** 2026-10-30T23:24:16Z
**Branch:** `main` (up to date with `origin/main`)
**Working tree:** clean (pycache gitignored)
**Last commits:** see `git log -5 --oneline`

## Initial Task (Start Here)

**PRIMARY GOAL:** Continue from the prior handoff (HANDOFF-2026-10-30T23-22-54Z.md). Replace the ill-conditioned SLSQP QP solves in `src/portfolio_opt.py` with a well-conditioned, deterministic solver (exact KKT active-set enumeration for N ≤ 5), then deliberately re-pin all affected artifacts. Get the primary verification gate green with re-pins visible in the diff.

This is the highest-value follow-up from the E049 fix (exit-status dependence removed, but tangency QP remains ill-conditioned causing golden drift).

## Repository State

Research phase complete (E001–E043). Five validated components: equity TSM flagship, DN low-beta sort, futures TSM 18m, futures realized-roll-yield carry, macro momentum. Market-neutral-total-portfolio line is CLOSED (E042 PARTIAL 4/5, E042b REJECTED 4/5).

`src/portfolio_opt.py` was fixed (E049): `max_sharpe` tangency branch and `project_onto_beta_cap` now judge solver answers on QP constraints via `_tangency_feasible`, never on `res.success`. `tests/test_portfolio_opt.py` added (5 tests, first-class in `scripts/check.sh`). One golden was deliberately re-pinned (E042 lead `/placebo_constrained`).

## Known Issues & Constraints

### 1) QP Ill-Conditioning (MUST FIX)
- **Symptom:** 1-ulp covariance perturbations move `min_var` weights by ~2.6e-05; E042-lead OOS Sharpe moves by ~3e-02 at 1e-14 perturbation.
- **Current drift vs goldens:** E041 portfolio (133 numeric), E041 grid (29), E042-primary (56), E042 grid (42) differences.
- **Approach:** Replace SLSQP solves with exact active-set enumeration over all KKT points for N ≤ 5 (reference oracle used). Ensure determinism and constraint satisfaction.
- **Critical:** Do NOT re-pin to silence drift without the solver change — that bakes machine-specific numbers over an unfixed defect. No research conclusion may change.

### 2) Second Defect (DO NOT FIX NOW)
- `y0 = w_feas / max(mu_s'w_feas, 1e-12)` at `src/portfolio_opt.py:253` masks negative denominator. At 2019-10-16 rebalance initial point magnitude 8.1e+11, violates `mu'y = 1` by 6.4e+09. SLSQP returns garbage (objective 3.7e+20), new feasibility check rejects it and falls back to LP vertex as golden did. Fixing would change published numbers — defer to same deliberate re-pin decision as (1).

### 3) E041 Residual Drift (INVESTIGATE ONLY IF NEEDED)
- 3 structural differences resolved ("8 of 96" stable; REJECTED 3/5 unchanged). 133 numeric remain from 1-ulp sensitivity. Only investigate if (1) does not collapse them.

## Execution Plan

1. **Understand current implementation** - Read `src/portfolio_opt.py` (tangency/max_sharpe, feasibility checks, fallbacks) and `tests/test_portfolio_opt.py`.
2. **Implement deterministic solver** - Add exact KKT enumeration for small N (N≤5). Validate feasibility on problem constraints. Replace SLSQP paths with this solver where appropriate; keep safe fallbacks.
3. **Test locally** - Run `python3 -m py_compile` on changed files. Run portfolio opt tests.
4. **Regenerate affected artifacts** - Re-run affected drivers (E041, E042 lead/grid as needed). Expect numeric changes from better conditioning.
5. **Deliberately re-pin** - Use `python3 scripts/check_golden_baseline.py --update` so replacements are visible in diff. Do NOT change tolerances/drivers/skips/research decisions.
6. **Verify gate** - Run `SEED=42 bash scripts/check.sh` then `SEED=42 python3 run_all_verification.py`. Must be green.

## Verification Commands (Run Before Declaring Done)

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Primary gate (~8 min; must be green)
SEED=42 python3 run_all_verification.py

# Confirm only intended source changes (pycache .pyc noise expected/ignorable)
git status --short | grep -v __pycache__
```

## Hard Rules (Do Not Violate)

- Always use `SEED=42`. Never move goalposts, change tolerances/drivers/skips, or change research decisions as side effect of verification.
- `experiments/*.json` are canonical; `run_all_verification.py` backs up and restores them — never commit verification output. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Replacing an artifact requires deliberate `scripts/check_golden_baseline.py --update` so replacement is in the diff.
- Offline mode: `QUANT_RESEARCH_OFFLINE=1`. Unpinned inputs fail hard (cache coverage invariant).
- Python 3; no separate linter — run `python3 -m py_compile` on changed files.
- CI workflow cannot be created by agents (controller restores `.github/workflows/`, token lacks push permission); template at `.github/workflow-templates/verification-gate.yml`.

## Session Completion Criteria

- Deterministic KKT-enumeration solver implemented in `src/portfolio_opt.py` and validated.
- Affected artifacts re-pinned deliberately via `scripts/check_golden_baseline.py --update` (all re-pins visible in diff).
- `scripts/check.sh` passes.
- Primary verification gate `run_all_verification.py` passes with `SEED=42`.
- No research conclusions changed. Working tree clean of unintended changes.
