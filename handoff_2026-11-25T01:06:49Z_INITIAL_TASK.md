# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T01:21:22Z
**Session**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043)**. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Important Notes

- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are committed artifacts - verification backs them up and restores after re-running
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current research status
3. Review any open issues or planned experiments
4. Verify baseline integrity before running experiments