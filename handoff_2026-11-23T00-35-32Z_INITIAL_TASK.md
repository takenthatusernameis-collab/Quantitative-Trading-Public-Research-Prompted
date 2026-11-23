# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T00:36:16Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State

- **Research Phase**: Complete (E001–E043)
- **Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Current Status**: Ready for next work session

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Important Notes

1. **Golden files**: `experiments/*.json` are canonical artifacts. Verification suite backs them up and restores after re-running.
2. **Reproducibility**: Always use `SEED=42` for walk-forward + placebo RNG.
3. **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is enforced.
4. **Baseline Integrity**: Never leave a verification run half-finished. Use `--restore-only` to recover if interrupted.
5. **No separate linter**: Run `python3 -m py_compile` on changed files.

## Next Steps for New Session

- Run `SEED=42 bash scripts/check.sh` to verify environment integrity
- Review `ledger/RESEARCH_LEDGER.md` for surviving validated strategies
- Check `ledger/golden_baseline.json` for pinned artifact fingerprints
- Consider any pending items from ledger (E045, E048, E049 open items)

---

*This handoff was created automatically at session start.*