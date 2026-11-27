# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T09:45:06Z
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

# Recovery after interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Integrity Notes
- `experiments/*.json` are canonical research artifacts — verification overwrites and restores them
- Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker
- Never leave a verification run half-finished; use `--restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` — do not re-pin without ledger entry

## Current State
- No active verification run detected
- All experiments committed at HEAD
- Ready for next session

## Next Steps (if any)
- Run `make check` to verify baseline integrity before starting work
- Consider running `make verify-quick` for quick validation
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies