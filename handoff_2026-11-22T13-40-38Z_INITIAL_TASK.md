# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T13:40:38Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

1. **Baseline Integrity**: `experiments/*.json` are canonical research artifacts. The verification suite overwrites them while re-running and restores them afterwards. A verification run must never be left half-finished.

2. **Reproducibility**: Always use `SEED=42` (walk-forward + placebo RNG).

3. **Data**: Cached parquet in `data/` (gitignored except pinned vintages). The 2026-10-12 vintage is pinned in `data/vintages.json`.

4. **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).

5. **Recovery**: If verification is interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.

## Current State

- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiment drivers have pre-registered JSON blocks with gates, falsification expectations, and sensitivity grids
- Verification suite is fully operational with convention robustness checks, golden baseline verification, and data coverage validation

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment and baseline integrity
2. Review `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Check `experiments/` for committed golden artifacts
4. Run verification suite as needed (`verify-quick`, `verify-extended`, or `verify-full`)
5. Any new experiments must follow pre-registration protocol with falsification expectations

---
*This handoff was created automatically at session initialization.*
