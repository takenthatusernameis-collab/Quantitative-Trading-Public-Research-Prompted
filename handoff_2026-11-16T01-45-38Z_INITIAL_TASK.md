# Agentic Work Session Handoff

**Timestamp**: 2026-11-16T01:46:07Z
**Session ID**: Initial handoff for next agentic session
**Project**: Quantitative-Trading-Public-Research-Prompted

## Project Status

**Research Phase**: Complete (E001–E043)
**Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`

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

## Key Integrity Notes

- **Golden artifacts**: `experiments/*.json` are canonical baselines — verification overwrites and restores them
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Never commit verification output** — restore goldens before committing
- **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`
- **Seed**: Always use `SEED=42` for reproducibility

## Outstanding Items (from ledger)

1. **E041 drift**: 133 numeric differences remain (1-ulp sensitivity of ill-conditioned QP) — do NOT re-pin
2. **E030**: Now offline-reproducible since 2026-10-20 (panel committed)
3. **E029**: Offline-reproducible since 2026-10-20 (fundamentals pinned)
4. **Optimizer determinacy**: `src/portfolio_opt.py` validates on constraints, not solver exit status (pinned by `tests/test_portfolio_opt.py`)

## Next Session Suggestions

- Run `make check` to verify baseline integrity before any work
- Consider running `make verify-quick` to confirm current state
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
- Any new experiments should follow pre-registration convention with falsification expectations

## Environment

- Python 3 with: numpy, pandas, scipy, pyarrow, statsmodels, yfinance
- Optional: cvxpy/cvxopt (falls back to scipy.optimize)
- Data cached in `data/` (gitignored except pinned vintages)