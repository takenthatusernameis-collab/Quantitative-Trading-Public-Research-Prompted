# HANDOFF: Next Agentic Work Session
**Timestamp (UTC):** 2026-10-29T08:15:31Z
**From:** Current session
**To:** Next agentic session
**Status:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## INITIAL TASK (Start here)
**Maintain baseline integrity; investigate and address the remaining numeric drift in E041/E042 from ill-conditioned QP (optimizer determinism).**

This is the only known open verification issue. All other guards pass. Do not re-pin goldens to silence QP conditioning drift without strong justification.

### Current State (verified at handoff time)
- Working tree clean; goldens match HEAD (`check_goldens_clean.py` exit 0).
- `SEED=42 bash scripts/check.sh` → ALL CHECKS PASSED.
- Quick verification: passes (8 drivers).
- Extended verification: drifts on E041 (133 numeric differences) and E042 (29 numeric differences) due to 1-ulp sensitivity of ill-conditioned tangency/min-var QP.
- Optimizer fix applied (E049): `src/portfolio_opt.py` validates constraints (not solver exit status). `tests/test_portfolio_opt.py` added as first-class guard.
- Golden baseline pinned in `ledger/golden_baseline.json` — never re-pin as side effect of verification.
- Data coverage enforced via `ledger/data_baseline.json`.

### What to do first (concrete)
1. Read `ledger/RESEARCH_LEDGER.md` (E049), `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`.
2. Confirm drift: `SEED=42 python3 run_all_verification.py --extended`.
3. Understand conditioning in `src/portfolio_opt.py`, `experiments/run_e041.py`, `experiments/run_e042.py`.
4. Explore numerical fixes (scaling/regularization/formulation) preserving feasibility/optimality; keep constraint validation passing.
5. Verify with `SEED=42 bash scripts/check.sh` and `--extended`; only consider tolerance updates with explicit ledger entry — never re-pin goldens.
6. Document findings in `ledger/RESEARCH_LEDGER.md`.

### Key Files
- `ledger/RESEARCH_LEDGER.md` (E049)
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`
- `experiments/run_e041.py`, `experiments/run_e042.py`
- `experiments/e041_*.json`, `experiments/e042_*.json`
- `run_all_verification.py`, `scripts/check.sh`

### Constraints
- Never re-pin goldens to silence numeric drift from ill-conditioned QP without strong justification.
- Follow all verification guards.
- Use `SEED=42` for all reproducibility runs.
- Research phase complete — focus on verification/infrastructure unless explicitly requested otherwise.

### Quick Commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --restore-only
```

## Handoff pointers (updated)
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-29T08-15-31Z.md`
Symlinks: `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md` -> this file
