# Agentic Work Session Handoff

**Timestamp**: 2026-11-20T09:40:12Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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
- **Golden files**: `experiments/*.json` are committed artifacts - verification backs them up and restores after re-running
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Dependencies**: `pip install -r requirements.txt`
- **Do not commit verification output** - restore before committing with `run_all_verification.py --restore-only`

## Current State

Repository is at a clean state ready for next research/experimentation session. All verification scripts and experiment drivers are in place per AGENTS.md conventions.