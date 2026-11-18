# Agentic Work Session Handoff

**Timestamp**: 2026-11-18T00:33:47Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
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
- **Golden files**: `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores them afterward
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- **Never commit verification output**: If a run is interrupted, restore with `run_all_verification.py --restore-only`

## Current Status

- Research phase complete (E001–E043)
- Verification suite operational
- Golden baseline integrity checks in place
- Convention robustness validation passing

## Next Steps for New Session

1. Run `make check` to verify convention robustness
2. Run `make verify-quick` for quick full verification
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Check `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` for baseline integrity

---

*This handoff was created automatically to provide context for the next agentic work session.*