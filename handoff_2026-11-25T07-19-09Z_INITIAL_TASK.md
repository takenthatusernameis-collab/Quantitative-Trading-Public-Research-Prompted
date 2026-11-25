# Handoff - 2026-11-25T07:20:33Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands (from AGENTS.md)
```bash
# Fast convention check
SEED=42 bash scripts/check.sh
# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

## Critical Notes
- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. Use `--restore-only` to recover if interrupted.
- **Golden baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against accidental baseline replacement.
- **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`. Cache coverage enforced via `scripts/check_data_coverage.py`.
- **Seed**: Always use `SEED=42` for reproducibility.
- **CI workflow**: Cannot be created by agents (permission restrictions). Template at `.github/workflow-templates/verification-gate.yml`.

## Current State
- No active verification run (checked: no `.verify_snapshot/ACTIVE.json`)
- All experiment drivers committed
- Ledger documents final dispositions (E042 PARTIAL, E025/E041 REJECTED, etc.)

## Next Steps (if continuing)
1. Run `SEED=42 python3 run_all_verification.py --skip-slow` for quick convention check
2. Or `SEED=42 python3 run_all_verification.py` for full quick verification
3. Check `ledger/RESEARCH_LEDGER.md` for strategy status before new experiments