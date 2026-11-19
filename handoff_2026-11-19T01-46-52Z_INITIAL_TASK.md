# Agentic Work Session Handoff

**Timestamp:** 2026-11-19T01:50:18Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Session Context

This is a quantitative trading research project with completed research phase (E001–E043). The surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands for Next Session

```bash
# Quick convention-robustness check + template validation
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

## Important Notes

- **Golden files** in `experiments/*.json` are canonical research artifacts
- Verification suite overwrites them during runs and restores afterward
- Never leave a verification run half-finished - use `--restore-only` to recover
- Cache coverage is enforced - `scripts/check_data_coverage.py` validates all data inputs
- SEED=42 must be used for reproducibility

## Next Steps

Review the verification status and determine if any experiments need re-running or if the ledger needs updates based on the latest validation results.