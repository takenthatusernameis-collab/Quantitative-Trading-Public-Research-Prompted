# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T11:04:29Z
**Session ID**: Initial session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Important Notes
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts. Verification backs them up before re-running and restores them afterward.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current experiment status
3. Review any open items in the ledger (E041 optimizer drift, E029/E030 pinned data)
4. Consider running verification suite to confirm reproducibility

## Active Issues / Open Items
- E041: 133 numeric differences remain (1-ulp sensitivity of ill-conditioned QP) - do not re-pin
- E042: Grid artifacts drift by 29-133 differences - do not re-pin
- E029/E030: Now offline-reproducible with pinned data vintages (2026-10-20)

---
*This handoff was created automatically at session initialization.*