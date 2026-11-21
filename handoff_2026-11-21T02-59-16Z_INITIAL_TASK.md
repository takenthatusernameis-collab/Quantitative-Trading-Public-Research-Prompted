# Agentic Work Session Handoff

**Timestamp:** 2026-11-21T03:01:44Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Session Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands for Next Session

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

- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are committed artifacts - verification backs them up and restores after re-running
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Recovery**: If verification interrupted, use `SEED=42 python3 run_all_verification.py --restore-only`

## Current Status

Research phase complete. All experiments pre-registered with falsification expectations. Verification suite available for reproduction.

---
*This handoff was created automatically for durable session continuity.*