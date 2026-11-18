# Agentic Work Session Handoff

**Timestamp**: 2026-11-18T10:27:42Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Artifacts

- **Golden files**: `experiments/*.json` - canonical research artifacts (never modified by verification)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` - surviving validated strategies
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Verification reports**: `.verify_reports/` (gitignored)

## Important Notes

1. **Seed**: Always use `SEED=42` for reproducibility
2. **Golden baseline integrity**: Verification suite backs up goldens before re-running and restores them afterward
3. **Never commit verification output**: If interrupted, restore with `run_all_verification.py --restore-only`
4. **Data coverage**: Enforced invariant - all data inputs must be pinned in `ledger/data_baseline.json`
5. **Optimizer determinicity**: Portfolio optimizer validates on problem constraints, not solver exit status (see ledger E049)

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Review any open items in the ledger (E041 drift, E049 optimizer determinism)
4. Consider running verification suite to confirm baseline integrity

---
*This handoff was created automatically at session start.*