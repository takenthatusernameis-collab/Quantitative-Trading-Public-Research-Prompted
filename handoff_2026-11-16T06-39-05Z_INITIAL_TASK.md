# Agentic Work Session Handoff

**Timestamp**: 2026-11-16T06:41:53Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. Research phase is complete. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are committed artifacts - never commit verification output
- **Recovery**: If verification is interrupted, run `SEED=42 python3 run_all_verification.py --restore-only`
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Dependencies**: `pip install -r requirements.txt`

## Verification Suite Behavior

The verification suite backs up golden files before re-running and restores them afterward. A verification run must never be left half-finished - the backup lives in `.verify_snapshot/` with an `ACTIVE.json` marker.

## Current Status

Ready for next agentic work session. No active tasks in progress.