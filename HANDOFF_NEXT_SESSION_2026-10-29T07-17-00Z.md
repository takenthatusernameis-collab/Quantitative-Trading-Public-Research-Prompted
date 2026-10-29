# HANDOFF: Next Agentic Work Session
**Timestamp (UTC):** 2026-10-29T07:17:00Z
**From:** Current session
**To:** Next agentic session
**Status:** Research phase complete (E001–E043). Surviving validated strategies documented in ledger/RESEARCH_LEDGER.md

## Immediate Priority
**Fix the remaining E041 drift issue / address optimizer determinism concerns.**

### Context
- E041 (market-neutral portfolio) was root-caused on 2026-10-20 (ledger E049): optimizer bug fixed (SLSQP status gating corrected to validate constraints, not solver exit status).
- Remaining drift: 133 numeric differences in E041 grid artifacts due to 1-ulp sensitivity of ill-conditioned QP. Extended verification still reports E041 as drifting.
- E042 (min-var confirmatory) also has similar numeric drift from ill-conditioned QP (29 differences).
- Do **NOT** re-pin E041/E042 to silence this - the ledger explicitly says see open item.

### Verification State
- Quick verification passes (8 drivers). Extended verification reports drift on E041 and E042 due to QP conditioning.
- Golden baseline is pinned in `ledger/golden_baseline.json` - must not be re-pinned as side effect of verification.
- Data coverage enforced via `ledger/data_baseline.json`.

### Key Files to Review
- `ledger/RESEARCH_LEDGER.md` - E049 entry for full context on optimizer determinism fix
- `src/portfolio_opt.py` - fixed optimizer validation logic
- `tests/test_portfolio_opt.py` - first-class test for constraint validation
- `run_all_verification.py` - verification orchestration
- `experiments/e041_*.json`, `experiments/e042_*.json` - artifacts with remaining drift

### Suggested Next Steps
1. Review E049 in ledger for full details of the optimizer fix
2. Understand the remaining QP conditioning issue - is there a way to make it more numerically stable without changing results?
3. Consider if tolerance needs adjustment or if there's a better formulation
4. Run `SEED=42 python3 run_all_verification.py --extended` to see current state
5. Document findings in ledger if changes made

### Constraints
- Never re-pin goldens to silence numeric drift from ill-conditioned QP without strong justification
- Follow all verification guards (check_goldens_clean, check_golden_baseline, check_data_coverage)
- Use SEED=42 for all reproducibility runs
- Research phase is complete - focus on verification/infrastructure issues or any explicit new requests

### Quick Commands
```bash
SEED=42 python3 run_all_verification.py --extended  # See current drift state
SEED=42 bash scripts/check.sh                        # Run all guards
git log --oneline -3                                # Recent commits
```

## Current handoff pointer
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-29T07-17-00Z.md` (see also `HANDOFF_CURRENT.md`, `HANDOFF.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md`).
