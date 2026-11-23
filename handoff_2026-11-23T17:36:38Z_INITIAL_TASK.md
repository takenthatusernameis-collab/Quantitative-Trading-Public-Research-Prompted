# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T17:40:10Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State Summary

**Research Phase**: Complete (E001–E043)
**Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`

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

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
#   or
make verify
```

## Critical Integrity Notes

1. **Golden Files**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites and restores them — never leave a verification run half-finished.

2. **Snapshot Recovery**: Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

3. **Baseline Protection**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` are first-class steps in `scripts/check.sh`. Never re-pin golden artifacts as a side effect of verification.

4. **Data Cache**: Cached parquet in `data/` (gitignored except pinned 2026-10-12/2026-10-11 vintages). E029 fundamentals pinned separately in `data/fundamentals/`. Cache coverage is an enforced invariant.

5. **Optimizer Determinism**: `src/portfolio_opt.py` validates on constraints, not solver exit status. E050 fix (exact KKT active-set enumeration) made E041/E042 bit-reproducible.

## Reproducibility Requirements

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Convention**: Close-to-close is v1.2.3 primary; overnight decomposition reported alongside
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Next Session Guidance

- Run `make check` first to verify environment integrity
- Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
- All experiment drivers have pre-registered JSON blocks with gates/falsification expectations
- Negative results recorded honestly (REJECTED / PARTIAL) with evidence
- Do not commit verification output — restore goldens before committing