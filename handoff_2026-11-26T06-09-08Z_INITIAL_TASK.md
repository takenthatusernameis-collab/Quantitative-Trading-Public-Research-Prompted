# Agentic Work Session Handoff

**Timestamp:** 2026-11-26T06:11:12Z
**Session ID:** [current session]
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Current State
- No active verification runs in progress
- Golden artifacts in `experiments/` are at HEAD (canonical baseline)
- No stale `.verify_snapshot/` pending

## Quick Commands Reference
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Recovery if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Integrity Notes
- **Never leave a verification run half-finished** — it overwrites `experiments/*.json` and restores after
- Run `scripts/check.sh` (or `make check`) before committing to catch golden mismatches
- Golden baseline pinned in `ledger/golden_baseline.json` — do not re-pin without ledger entry
- Data cache coverage enforced via `scripts/check_data_coverage.py` against `ledger/data_baseline.json`

## Next Session Guidance
1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. If running verification, use appropriate tier (`--skip-slow` for convention-only)
4. Always restore goldens after interrupted runs before committing

---
*This handoff was created automatically at session start for durability across agentic sessions.*