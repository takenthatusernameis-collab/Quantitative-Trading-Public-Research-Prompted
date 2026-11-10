# Agentic Work Session Handoff

**Timestamp:** 2026-11-10T22:38:51Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands

```bash
# Convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Important Notes

- **Golden files:** `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores them afterward.
- **Do not commit verification output:** If a run is interrupted, restore with `run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Seed:** Always use `SEED=42` (walk-forward + placebo RNG)
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Next Session Guidance

Review `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items. The verification suite is the primary quality gate.