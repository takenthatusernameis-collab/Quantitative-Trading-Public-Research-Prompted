# Agent Handoff — 2026-11-17T12:49:45Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands (from AGENTS.md)
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Critical Notes
1. **Golden files**: `experiments/*.json` are canonical artifacts. Verification overwrites and restores them — never leave a run half-finished.
2. **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Baseline integrity**: `scripts/check_golden_baseline.py` compares artifacts to SHA-256 in `ledger/golden_baseline.json`. Re-pinning requires explicit `--update`.
4. **Data cache**: Pinned vintages in `data/vintages.json` (2026-10-12) and `data/fundamentals_vintages.json` (E029). Cache coverage enforced by `scripts/check_data_coverage.py`.
5. **Seed**: Always use `SEED=42` for reproducibility.
6. **CI**: Workflow template at `.github/workflow-templates/verification-gate.yml` — must be created manually via GitHub UI.

## Open Items (from Ledger)
- E041 optimizer drift (133 numeric diffs, ill-conditioned QP) — do not re-pin
- E042 grid artifacts drift (29–133 diffs) — do not re-pin
- See `ledger/RESEARCH_LEDGER.md` entries E045, E048, E049

## Next Steps
- Run `make check` to verify convention robustness
- Run `make verify-quick` for full quick verification
- Check `ledger/RESEARCH_LEDGER.md` for surviving strategy documentation