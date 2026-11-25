# Handoff - Next Agentic Work Session

**Timestamp**: 2026-11-25T06:17:13Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial Task
No specific task assigned for the next agentic work session. Repository is at a clean, verified state ready for the next instruction.

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Notes
- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are committed artifacts - never commit verification output
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Offline mode**: `QUANT_RESEARCH_OFFLINE=1` enforced during verification
- **Baseline integrity**: Run `scripts/check.sh` before committing to verify golden files match HEAD

## Current Status
No active verification run. Repository is at a clean state ready for next task.
