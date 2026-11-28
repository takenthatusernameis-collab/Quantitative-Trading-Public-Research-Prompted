# Agentic Work Session Handoff

**Timestamp**: 2026-11-28T02:46:48Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
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

## Key Notes
- Always use `SEED=42` for reproducibility
- Golden files in `experiments/*.json` are canonical artifacts
- Verification suite backs up goldens before re-running and restores them afterward
- Never commit verification output; restore with `--restore-only` if interrupted
- Data cached in `data/` (gitignored except pinned vintages)
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

## Recent State
- Research phase complete (E001–E043)
- Ledger documents surviving validated strategies
- E050 fix (exact KKT active-set enumeration) made E041/E042 bit-reproducible
- All 18 extended drivers reproduce with 0 differences (measured 2026-11-23T05:17Z)