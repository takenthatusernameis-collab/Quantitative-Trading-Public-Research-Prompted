# Agentic Work Session Handoff

**Timestamp**: 2026-11-28T10:36:38Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
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

## Key Notes for Next Session
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are canonical research artifacts - verification overwrites and restores them
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- **Never commit verification output** - if interrupted, run `run_all_verification.py --restore-only`

## Recent Verification Status
- Last extended verification: 2026-11-23T05:17Z (numpy 2.5.4, scipy 1.18.1) - all 18 extended drivers reproduce with 0 differences
- E050 fix (exact KKT active-set enumeration) made E041/E042 bit-reproducible
- E029 fundamentals snapshot pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- E030 16-ETF input panel committed and golden re-pinned

## Pending/Next Tasks
- [ ] Review any new experiment ideas or follow-up research directions
- [ ] Consider promoting any PARTIAL strategies to confirmatory runs
- [ ] Monitor for any dependency updates that might affect reproducibility