# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T08:12:44Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

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
- **Golden files**: `experiments/*.json` are canonical research artifacts. The verification suite backs them up before re-running and restores them afterward.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). The 2026-10-12 vintage is pinned in `data/vintages.json`.
- **Baseline integrity**: A verification run must never be left half-finished. If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` to recover.
- **Do not commit verification output**: Restore goldens before committing.

## Next Steps for New Session

1. Run `make check` to verify environment and baseline integrity
2. Review `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Check `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` for any pending issues
4. Consider running `make verify-quick` for a full verification cycle

## Open Items (from ledger)

- E041 drift: 133 numeric differences remain (1-ulp sensitivity of ill-conditioned QP) — do not re-pin
- E042 grid artifacts still drift by 29-133 differences — do not re-pin
- CI workflow template exists at `.github/workflow-templates/verification-gate.yml` but requires maintainer to create via GitHub UI