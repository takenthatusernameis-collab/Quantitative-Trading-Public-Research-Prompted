# Agent Handoff — 2026-11-14T20:27:45Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043); surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min + 96-config grid)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes
- **Golden files**: `experiments/*.json` are canonical artifacts. Verification overwrites then restores them.
- **Never leave verification half-finished** — use `--restore-only` to recover if interrupted.
- **Baseline integrity**: `scripts/check_golden_baseline.py` compares against SHA-256 in `ledger/golden_baseline.json`
- **Cache coverage**: All data inputs must be pinned in `ledger/data_baseline.json`
- **Seed**: Always use `SEED=42` for reproducibility

## Recent State
- E042 (min-var confirmatory): PARTIAL
- E041 (market-neutral): REJECTED (optimizer drift documented in ledger E049)
- E029, E030: Now offline-reproducible with pinned data vintages (ledger E048)
- CI workflow template at `.github/workflow-templates/verification-gate.yml` (maintainer must create actual workflow)

## Next Steps
- Run `make check` to verify convention robustness
- Consider `verify-extended` if structural changes made
- Review `ledger/RESEARCH_LEDGER.md` for open items before new experiments