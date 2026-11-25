# Handoff - Next Agentic Work Session

**Timestamp**: 2026-11-25T16:34:17Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py

# Restore golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Notes
- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are committed artifacts - never commit verification output
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Offline mode**: `QUANT_RESEARCH_OFFLINE=1` enforced during verification
- **Baseline integrity**: Run `scripts/check.sh` before committing to verify golden files match HEAD

## Current Status
Working tree is clean on `main`. No active verification run. Repository is at a clean state ready for next task. Recent commits are `chore(kilo): checkpoint agent session`.
