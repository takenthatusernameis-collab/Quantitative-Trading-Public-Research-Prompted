# HANDOFF: Next Agentic Work Session
**Timestamp (UTC):** 2026-10-29T08-11-29Z
**From:** Current session
**To:** Next agentic session
**Status:** Research phase complete (E001–E043). Surviving validated strategies documented in ledger/RESEARCH_LEDGER.md

## INITIAL TASK (Start here)
**Investigate and address the remaining numeric drift in E041/E042 from ill-conditioned QP (optimizer determinism).**

This is the only known open verification issue. All other guards pass; do not re-pin goldens to silence QP conditioning drift.

### Current State (verified)
- Quick verification: passes (8 drivers: E012, E023, E024--merge, E027, E035, E037, E039, E042-lead)
- Extended verification: drifts on E041 (133 numeric differences) and E042 (29 numeric differences) due to 1-ulp sensitivity of ill-conditioned tangency/min-var QP
- Optimizer fix applied (E049): `src/portfolio_opt.py` now validates constraints (not solver exit status). `tests/test_portfolio_opt.py` added as first-class guard.
- Golden baseline pinned in `ledger/golden_baseline.json` — never re-pin as side effect of verification
- Data coverage enforced via `ledger/data_baseline.json` (all driver inputs pinned/cached)

### What to do first (concrete)
1. **Read context**: `ledger/RESEARCH_LEDGER.md` (E049) and `src/portfolio_opt.py` + `tests/test_portfolio_opt.py`
2. **Confirm drift state**: `SEED=42 python3 run_all_verification.py --extended` (observe E041/E042 diff counts)
3. **Understand conditioning**: Look at how tangency/min-var QP is formulated in `src/portfolio_opt.py` and where E041/E042 build the optimization problem (check drivers `experiments/run_e041.py`, `experiments/run_e042.py`)
4. **Explore numerical fixes** (without changing economic results): consider scaling/regularization, better conditioning, solver options, or formulation changes that preserve feasibility/optimality to within acceptable precision. Any change must keep constraint validation passing.
5. **Verify**: Run `SEED=42 bash scripts/check.sh` and `SEED=42 python3 run_all_verification.py --extended`. If drift reduces below tolerance or becomes explainable with justification, only then consider updating tolerances with explicit ledger entry — **do not** re-pin goldens.
6. **Document**: Update `ledger/RESEARCH_LEDGER.md` with findings/changes.

### Key Files
- `ledger/RESEARCH_LEDGER.md` (E049)
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`
- `experiments/run_e041.py`, `experiments/run_e042.py`
- `experiments/e041_*.json`, `experiments/e042_*.json`
- `run_all_verification.py`, `scripts/check.sh`

### Constraints
- Never re-pin goldens to silence numeric drift from ill-conditioned QP without strong justification
- Follow all verification guards (check_goldens_clean, check_golden_baseline, check_data_coverage)
- Use `SEED=42` for all reproducibility runs
- Research phase complete — focus on verification/infrastructure unless explicitly requested otherwise

### Quick Commands
```bash
SEED=42 python3 run_all_verification.py --extended  # See current drift state
SEED=42 bash scripts/check.sh                        # Run all guards
git log --oneline -3                                # Recent commits
```

## Handoff pointers (updated)
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-29T08-07-24Z.md`
Symlinks: `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md` -> this file
