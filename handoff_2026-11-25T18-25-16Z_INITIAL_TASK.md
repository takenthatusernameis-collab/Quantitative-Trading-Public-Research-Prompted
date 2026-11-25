# Agentic Work Session Handoff

**Timestamp:** 2026-11-25T19:36:09Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State

- **Research Phase:** Complete (E001–E043)
- **Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Verification Suite:** Ready to run (see AGENTS.md for commands)

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Important Notes

1. **Baseline Integrity:** `experiments/*.json` are canonical artifacts. Verification overwrites and restores them. Never leave a verification run half-finished.

2. **Recovery:** If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Reproducibility:** Always use `SEED=42`. Data cached in `data/` (gitignored except pinned vintages).

4. **CI Gate:** Template at `.github/workflow-templates/verification-gate.yml` — must be created manually via GitHub UI.

## Next Steps for New Session

- Run `make check` to verify baseline integrity before any changes
- Review `ledger/RESEARCH_LEDGER.md` for surviving validated strategies
- Check `scripts/check_golden_baseline.py` and `scripts/check_data_coverage.py` for artifact/data integrity