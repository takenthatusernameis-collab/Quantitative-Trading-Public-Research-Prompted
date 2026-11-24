# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T03:11:09Z
**Session**: Initial handoff for next agentic work session

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
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

## Key Notes
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores them afterward.
- **Do not commit verification output**: If a run is interrupted, restore with `run_all_verification.py --restore-only`
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current experiment status
3. Review any open issues or tasks in the codebase