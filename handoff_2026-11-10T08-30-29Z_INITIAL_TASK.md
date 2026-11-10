# Handoff Message

**Timestamp:** 2026-11-10T10:24:09Z
**Session:** Agentic work session initialization

## Project Context
Quantitative Trading Public Research (2014-2026 US equities, futures, macro data)
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`

## Quick Commands
```bash
# Fast convention-robustness check
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Points for Next Session
- Golden files in `experiments/*.json` are canonical artifacts
- Verification suite backs up and restores them automatically
- Use `SEED=42` for reproducibility
- Data cached in `data/` (gitignored except pinned vintages)
- Dependencies: `pip install -r requirements.txt`

## Current State
No active verification run. Ready for next task.