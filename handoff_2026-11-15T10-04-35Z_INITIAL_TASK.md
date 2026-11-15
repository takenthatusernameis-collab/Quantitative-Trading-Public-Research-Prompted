# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T10:08:04Z
**Session ID**: Initial handoff created by user request
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. Research phase is complete.

**Key Artifacts**:
- `ledger/RESEARCH_LEDGER.md` - Documents surviving validated strategies
- `experiments/*.json` - Canonical research artifacts (golden files)
- `data/` - Cached parquet data (gitignored except pinned vintages)
- `src/` - Core research modules

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

## Important Notes

- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores them afterward.
- **Never commit verification output**: If a run is interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Data**: Cached in `data/` with pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`
- **Cache coverage is enforced**: `scripts/check_data_coverage.py` validates all data inputs are pinned

## Current State

- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Verification suite operational with quick/extended/full modes
- CI gate template available at `.github/workflow-templates/verification-gate.yml` (maintainer must create actual workflow)

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Run verification suite as needed (`make verify-quick`, `make verify-extended`, `make verify-full`)
4. Any new experiments should follow pre-registration protocol with falsification expectations

---
*This handoff was created automatically at session start. Update as needed for subsequent sessions.*