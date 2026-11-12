# Agent Handoff — 2026-11-12T00:27:09Z

## Session Context
- **Project**: Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043), surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Verification Commands
```bash
# Fast check (~seconds)
SEED=42 bash scripts/check.sh
# or: make check

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# or: make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or: make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or: make verify-full
```

## Critical Integrity Notes
- `experiments/*.json` are canonical goldens — verification overwrites and restores them
- Never leave a verification run half-finished (use `--restore-only` to recover)
- Golden baseline pinned in `ledger/golden_baseline.json` — do not re-pin without ledger approval
- Cache coverage enforced via `scripts/check_data_coverage.py` — all inputs must be pinned

## Current State
- No active verification run detected
- All goldens should match HEAD
- Ready for next task (new experiment, verification, analysis, etc.)

## Next Steps (suggested)
- Run `make check` to verify baseline integrity
- Run `make verify-quick` for fast regression check
- Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
- Review open items: E041 optimizer drift (133 numeric diffs), E042 grid sensitivity

---
*Generated automatically for durable session handoff*