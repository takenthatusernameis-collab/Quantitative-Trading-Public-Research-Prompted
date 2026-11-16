# Handoff — 2026-11-16T13:32:32Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043), surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands
```bash
# Fast check (convention robustness + template validation)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes
- **Golden files**: `experiments/*.json` are canonical artifacts — never commit verification output
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Seed**: Always use `SEED=42` for reproducibility
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Cache coverage**: Enforced invariant — `scripts/check_data_coverage.py` validates all downloads

## Verification Suite Behavior
- Backs up goldens to `.verify_snapshot/` with `ACTIVE.json` marker (pid)
- Restores on completion/interrupt
- Compares against `ledger/golden_baseline.json` SHA-256 pins
- Extended drift report → `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored)

## Known Drift (reporting only)
- E030: 28 numeric diffs on near-zero quantities (pinned 2026-10-20, ledger E048)
- E041: 133 numeric diffs (1-ulp QP sensitivity, optimizer defect fixed, ledger E049)
- E042 grid artifacts drift similarly — do NOT re-pin to silence

## Next Steps
- Run `make check` to validate current state
- Run `make verify-quick` for full quick verification
- Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items