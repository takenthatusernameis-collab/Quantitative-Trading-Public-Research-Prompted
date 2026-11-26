# Agentic Work Session Handoff

**Timestamp:** 2026-11-26T04:27:08Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. Research phase is complete. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

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

- **Golden files**: `experiments/*.json` are canonical research artifacts. The verification suite backs them up before re-running and restores them afterward.
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG).
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). The 2026-10-12 vintage is pinned in `data/vintages.json`.
- **Baseline Integrity**: A verification run must never be left half-finished. If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` to recover.
- **Convention**: Close-to-close is the v1.2.3 primary convention. Overnight decomposition is reported alongside for every strategy.

## Next Steps / Available Tasks

1. Run verification suite (`make verify-quick`, `make verify-extended`, or `make verify-full`)
2. Run individual experiment drivers (E025, E041, E042, etc.)
3. Run batch validation (`SEED=42 python3 src/batch_run.py --universe large_liquid`)
4. Check convention robustness (`make verify`)
5. Review ledger at `ledger/RESEARCH_LEDGER.md` for surviving strategies

## Git Status

Repository is clean. No uncommitted changes.