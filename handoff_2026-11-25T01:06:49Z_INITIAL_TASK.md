# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T01:11:16Z
**Session ID**: Initial handoff created by Kilo
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

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

1. **Baseline Integrity**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them while re-running and restores afterward. Never leave a verification run half-finished.

2. **Recovery**: If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Golden Baseline**: `ledger/golden_baseline.json` contains SHA-256 fingerprints of all tracked artifacts. Never re-pin as side effect of verification.

4. **Data Cache**: Cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`.

5. **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). cvxpy/cvxopt optional.

## Current Status

- Research phase complete (E001–E043)
- All experiment drivers committed
- Verification suite operational
- No active verification run in progress

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for surviving strategies
3. Run verification suite as needed (`verify-quick`, `verify-extended`, or `verify-full`)
4. Review any new experiment ideas against pre-registration requirements

---
*This handoff was created automatically. Update with session-specific context as work progresses.*