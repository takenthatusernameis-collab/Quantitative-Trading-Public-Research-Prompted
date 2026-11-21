# Agentic Work Session Handoff

**Timestamp**: 2026-11-21T19:11:52Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands for Next Session

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

## Important Notes for Next Session

1. **Golden files**: `experiments/*.json` are committed artifacts. The verification suite backs them up before re-running and restores them afterward — the baseline is never modified by verification.

2. **Do not commit verification output**: If a run is interrupted, the working tree holds driver output instead of the goldens. Restore before committing (`run_all_verification.py --restore-only`).

3. **Reproducibility**: Always use `SEED=42` (walk-forward + placebo RNG).

4. **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.

5. **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).

## Next Steps

The next agentic session should:
1. Run `make check` to verify the current state
2. Run `make verify-quick` for quick verification if needed
3. Check `ledger/RESEARCH_LEDGER.md` for current experiment statuses
4. Continue any pending research tasks or validation work

---
*This handoff was created automatically at session initialization.*