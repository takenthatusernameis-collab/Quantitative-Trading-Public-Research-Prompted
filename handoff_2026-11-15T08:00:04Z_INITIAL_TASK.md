# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T08:00:04Z
**Session**: Initial handoff for next agentic work session
**Workspace**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Project Context

This is a quantitative trading research repository covering 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
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

## Important Notes

- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are committed artifacts - never commit verification output
- **Recovery**: If verification is interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is enforced via `scripts/check_data_coverage.py`
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Current State

- Research phase complete (E001–E043)
- Ledger documents surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- Verification suite validates reproducibility across multiple experiment drivers
- Convention robustness check validates close-to-close v1.2.3 primary convention with overnight decomposition

## Next Steps for New Session

1. Run `make check` to verify current state
2. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
3. Check `experiments/` for golden baseline artifacts
4. Consider running `make verify-quick` for full verification if needed

---
*This handoff was created automatically at session start. Update as needed for subsequent sessions.*
