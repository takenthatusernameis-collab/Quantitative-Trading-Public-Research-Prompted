# Handoff for Next Agentic Work Session

**Timestamp:** 2026-11-25T05:26:13Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

This is a quantitative trading research repository with completed research phase (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes

1. **Golden files**: `experiments/*.json` are committed artifacts. The verification suite backs them up before re-running and restores them afterward.
2. **Never commit verification output**: If a run is interrupted, restore with `run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Seed**: Always use `SEED=42` for reproducibility
4. **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.

## Current State

- Research phase complete (E001–E043)
- All experiments pre-registered with falsification expectations
- Verification suite handles baseline integrity with `.verify_snapshot/` recovery mechanism
- CI gate template exists at `.github/workflow-templates/verification-gate.yml` (maintainer must create actual workflow)

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Use verification commands above as needed
4. Any new experiments must follow pre-registration convention