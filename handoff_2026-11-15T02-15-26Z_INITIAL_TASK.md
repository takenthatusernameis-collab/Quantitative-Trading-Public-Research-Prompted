# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T02:16:44Z
**Session ID**: Initial handoff for next session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is a quantitative trading research repository focused on reproducible strategy research on 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

1. **Golden files**: `experiments/*.json` are canonical research artifacts. The verification suite backs them up before re-running and restores them afterward.
2. **Never commit verification output**: If a run is interrupted, restore with `python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Seed**: Always use `SEED=42` for reproducibility
4. **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is enforced by `scripts/check_data_coverage.py`

## Next Steps for New Session

- Run `SEED=42 bash scripts/check.sh` to verify environment integrity
- Review `ledger/RESEARCH_LEDGER.md` for current strategy statuses
- Check `AGENTS.md` for full project conventions and commands

## Current State

- Research phase: COMPLETE (E001–E043)
- Validation: Surviving strategies documented in ledger
- Verification suite: Ready for execution
- Golden baseline: Pinned in `ledger/golden_baseline.json`
- Data baseline: Pinned in `ledger/data_baseline.json`