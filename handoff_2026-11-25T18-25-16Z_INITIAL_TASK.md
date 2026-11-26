# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T02:24:20Z
**Session**: Initial task message for next agentic work session
**Project**: Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Verification Commands

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

- **Golden files**: `experiments/*.json` (canonical research artifacts)
- **Data cache**: `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (surviving validated strategies)
- **Golden baseline**: `ledger/golden_baseline.json` (SHA-256 fingerprints)
- **Data baseline**: `ledger/data_baseline.json` (SHA-256 for cache coverage)

## Important Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
2. **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against accidental baseline replacement
3. **Cache coverage**: `scripts/check_data_coverage.py` enforces all data inputs are pinned
4. **Seed**: Always use `SEED=42` for reproducibility
5. **Convention**: Close-to-close is v1.2.3 primary; overnight decomposition reported alongside

## Recent Ledger Entries

- **E049**: Optimizer determinism fix — SLSQP status-gating removed, validated on constraints
- **E050**: Exact KKT active-set enumeration as primary tangency solver — bit-reproducible artifacts
- **E045**: E029 fundamentals snapshot pinned — offline reproducible
- **E048**: E030 16-ETF panel committed — offline reproducible

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Run verification suite as needed (`verify-quick`, `verify-extended`, `verify-full`)
4. Any new experiments require pre-registration with falsification expectations and promotion gates