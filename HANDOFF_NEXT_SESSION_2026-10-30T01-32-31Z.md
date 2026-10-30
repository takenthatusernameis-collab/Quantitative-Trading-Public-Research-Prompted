# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-30T01:32:31Z
**From:** Glyph Cluster (current session)
**To:** Next agentic session
**Status:** Ready for handoff

## Initial Task (Clear & Actionable)

**Task:** Continue from the most recent open research/engineering item - fix the tangency QP ill-conditioning to restore full reproducibility of E041/E042 grid artifacts without breaking the solver-status fix.

## Context

The optimizer determinism fix (E049) is in place:
- `src/portfolio_opt.py` now validates answers against problem constraints (not solver `success` status).
- `tests/test_portfolio_opt.py` added and passes; integrated into `scripts/check.sh`.
- E042 lead primary now matches golden to 5e-9. E041 structural diffs resolved. E042 lead placebo block was deliberately re-pinned (documented in ledger).
- Remaining: tangency QP is ill-conditioned (1-ulp perturbations move `min_var` answers by ~1e-5). E041/E042 grid artifacts still drift (29-133 diffs) vs goldens; not re-pinned.

## Concrete Next Steps

1. **Investigate well-conditioned solver approach**
   - For small N (N<=5 assets in tangency/market-neutral configs), consider exact active-set enumeration of all KKT points as reference (used to debug).
   - Evaluate replacing SLSQP with a more stable method (e.g., CVXOPT/OSQP if available, or custom active-set) while keeping constraints identical.
   - Preserve feasibility validation and the "accept if feasible even if status!=success" invariant.

2. **Fix the denominator masking issue** (separate, deliberate re-pin decision)
   - `y0 = w_feas / max(mu_s'w_feas, 1e-12)` in `src/portfolio_opt.py:253` masks negative denominator causing bad initialization at 2019-10-16. Fix to proper max-mu_s'w LP initialization. This will change numbers - plan for deliberate re-pin with justification in ledger.

3. **Validate changes**
   - Run `SEED=42 bash scripts/check.sh` (must pass, including new portfolio_opt tests)
   - Run relevant drivers: `SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e041.py` and `SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e042_lead.py` (and grids as needed)
   - Compare against goldens with same tolerances; if differences remain only in expected exploratory counts or are resolved, document in ledger.

4. **Update ledger**
   - Record findings in `ledger/RESEARCH_LEDGER.md` under E049 or new entry. Follow existing style (hypothesis, change, measured effect, constraints honored). If re-pinning goldens, use `scripts/check_golden_baseline.py --update` and document rationale per precedent.

## Guardrails
- Follow AGENTS.md: SEED=42, offline mode for drivers (`QUANT_RESEARCH_OFFLINE=1`), never re-pin to silence environment defects without justification, keep verification suite intact.
- Do not commit verification artifacts mid-run. If interrupted, use `run_all_verification.py --restore-only`.
- Honor "judge answer on problem, not solver status" invariant.
- No goalpost moves; decisions unchanged unless evidence forces (and pre-registered).

## Quick References
- Ledger: `ledger/RESEARCH_LEDGER.md` (E049)
- Code: `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`
- Verification: `scripts/check.sh`, `run_all_verification.py`
- Golden checks: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`

## Success Criteria
- E041/E042 artifacts reproduce to within tolerance (or differences explained and goldens deliberately re-pinned with ledger entry), without reintroducing solver-status dependence.
- All checks pass (`scripts/check.sh`).
- Changes documented in ledger with measured effects.
