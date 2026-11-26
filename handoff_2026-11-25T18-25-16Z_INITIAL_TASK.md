# Agentic Work Session Handoff

**Timestamp:** 2026-11-26T02:34:36Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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

- **Golden files**: `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores them afterward.
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG).
- **Baseline integrity**: Never leave a verification run half-finished. Use `--restore-only` to recover if interrupted.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is enforced invariant.
- **Optimizer determinacy**: `src/portfolio_opt.py` validates solver answer on problem constraints, not solver exit status (ledger E049). E050 fix (exact KKT active-set enumeration) makes E041/E042 bit-reproducible.

## Pending / Next Steps

No specific pending tasks identified. Next session can:
1. Run verification suite (`make verify-quick` or `make verify-full`)
2. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
3. Explore experiment drivers in `experiments/run_e*.py`
4. Check `src/` for core library code

## Key Files to Review

- `AGENTS.md` - Project commands & conventions
- `ledger/RESEARCH_LEDGER.md` - Validated strategies
- `ledger/golden_baseline.json` - Pinned SHA-256 fingerprints
- `scripts/check_golden_baseline.py` - Baseline integrity guard
- `scripts/check_data_coverage.py` - Data cache coverage enforcement

---

*This handoff was created automatically at session start. Update as needed during work.*