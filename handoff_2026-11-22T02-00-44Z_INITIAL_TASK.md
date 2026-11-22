# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T02:01:29Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Session Context

This is a quantitative trading research project covering 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Important Notes

- Always use `SEED=42` for reproducibility
- Golden files in `experiments/*.json` are canonical artifacts
- Verification suite backs up goldens before re-running and restores after
- Never commit verification output; restore with `--restore-only` if interrupted
- Data cached in `data/` (gitignored except pinned vintages)
- Cache coverage is enforced invariant (ledger E048)

## Next Steps

Resume verification or run individual experiment drivers as needed.