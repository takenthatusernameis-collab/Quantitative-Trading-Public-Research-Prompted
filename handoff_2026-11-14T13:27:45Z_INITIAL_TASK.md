# Agentic Work Session Handoff

**Timestamp**: 2026-11-14T13:28:29Z
**Session**: Initial handoff for next agentic work session
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Notes

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores them afterward.
- **Data**: Cached parquet in `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages)
- **Cache coverage**: Enforced invariant - all `data.download()` call sites must have committed cache files matching SHA-256 in `ledger/data_baseline.json`
- **Do not commit verification output**: If run interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only`

## Current State

No active verification run in progress. Repository is at baseline state ready for next session.