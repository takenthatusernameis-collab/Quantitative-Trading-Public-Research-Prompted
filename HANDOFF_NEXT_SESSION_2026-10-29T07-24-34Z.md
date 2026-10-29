# HANDOFF: Next Agentic Work Session
**Timestamp (UTC):** 2026-10-29T07:24:34Z
**From:** Current session
**To:** Next agentic session
**Status:** Research phase complete (E001–E043). Surviving validated strategies documented in ledger/RESEARCH_LEDGER.md

## Immediate Priority
**Address remaining E041/E042 numeric drift from ill-conditioned QP (optimizer determinism).**

### Context
- E041 (market-neutral portfolio) root-caused on 2026-10-20 (ledger E049): optimizer bug fixed — SLSQP status gating corrected to validate constraints, not solver exit status (`src/portfolio_opt.py`).
- Remaining drift: 133 numeric differences in E041 grid artifacts due to 1-ulp sensitivity of ill-conditioned QP. Extended verification still reports E041 as drifting.
- E042 (min-var confirmatory) similar drift from ill-conditioned QP (29 differences).
- Do **NOT** re-pin E041/E042 to silence this — the ledger explicitly marks it an open item.

### Verification State
- Quick verification passes (8 drivers: E012, E023, E024--merge, E027, E035, E037, E039, E042-lead).
- Extended verification reports drift on E041 (133 diffs) and E042 (29 diffs) due to QP conditioning.
- Golden baseline pinned in `ledger/golden_baseline.json` — must not be re-pinned as a side effect of verification.
- Data coverage enforced via `ledger/data_baseline.json` (all driver inputs pinned/cached).

### Key Files to Review
- `ledger/RESEARCH_LEDGER.md` — E049 entry (optimizer determinism fix + open item)
- `src/portfolio_opt.py` — fixed optimizer validation logic
- `tests/test_portfolio_opt.py` — first-class test for constraint validation
- `run_all_verification.py` — verification orchestration
- `experiments/e041_*.json`, `experiments/e042_*.json` — artifacts with remaining drift

### Suggested Next Steps
1. Review E049 in ledger for full context on the optimizer fix
2. Investigate whether QP conditioning can be improved numerically without changing results
3. Consider tolerance adjustment or better formulation for ill-conditioned tangency/min-var QP
4. Run `SEED=42 python3 run_all_verification.py --extended` to confirm current drift state
5. Run `SEED=42 bash scripts/check.sh` to confirm all guards pass
6. Document any changes in `ledger/RESEARCH_LEDGER.md`

### Constraints
- Never re-pin goldens to silence numeric drift from ill-conditioned QP without strong justification
- Follow all verification guards (check_goldens_clean, check_golden_baseline, check_data_coverage)
- Use `SEED=42` for all reproducibility runs
- Research phase is complete — focus on verification/infrastructure or explicit new requests only

### Quick Commands
```bash
SEED=42 python3 run_all_verification.py --extended  # See current drift state
SEED=42 bash scripts/check.sh                        # Run all guards
git log --oneline -3                                # Recent commits
```

## Current handoff pointer
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-29T07-24-34Z.md` (see also `HANDOFF_CURRENT.md`, `HANDOFF.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md`).
