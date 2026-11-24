# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T15:59:46Z
**Session ID**: Initial handoff for next session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is a quantitative trading research repository covering 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Important Notes

- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are canonical artifacts - verification overwrites and restores them
- **Never commit verification output** - restore with `--restore-only` if interrupted
- **Cache coverage**: Enforced invariant - all data inputs must be pinned
- **Optimizer determinicity**: Exact KKT active-set enumeration (E050 fix) ensures bit-reproducibility

## Current State

- Research complete (E001-E043)
- Ledger documents surviving strategies in `ledger/RESEARCH_LEDGER.md`
- Verification suite validates reproducibility across all experiments
- Data cached in `data/` (gitignored except pinned vintages)

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Run verification suite as needed (`verify-quick`, `verify-extended`, `verify-full`)
4. Any new experiments must follow pre-registration protocol

---
*This handoff was created automatically at session start.*