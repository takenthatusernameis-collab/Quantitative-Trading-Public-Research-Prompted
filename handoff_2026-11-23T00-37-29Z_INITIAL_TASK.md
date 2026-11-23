# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T00:37:29Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State

- **Research Phase**: Complete (E001–E043)
- **Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Current Status**: Ready for next work session; working tree clean except `__pycache__` .pyc files (untracked/modified pyc, not source)

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min; 8 drivers in 5a block)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; quick + 18 committed drivers)
SEED=42 python3 run_all_verification.py --extended

# Single compile check on changed files
python3 -m py_compile <changed_file>.py
```

## Important Notes

1. **Golden files**: `experiments/*.json` are canonical artifacts. Verification suite backs them up and restores after re-running — never leave a run half-finished.
2. **Reproducibility**: Always use `SEED=42` (walk-forward + placebo RNG).
3. **Baseline Integrity**: If verification was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
4. **Data coverage**: `scripts/check_data_coverage.py` requires every `data.download()` call site to have a pinned, git-tracked cache file matching `ledger/data_baseline.json`. Unpinned inputs = live network download (fails under `QUANT_RESEARCH_OFFLINE=1`).
5. **Optimizer determinism**: `src/portfolio_opt.py` validates solver answers on constraints, not exit status — see `tests/test_portfolio_opt.py`.

## Next Steps for New Session

- Run `SEED=42 bash scripts/check.sh` to verify environment integrity
- Review `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items (E045, E048, E049)
- Check `ledger/golden_baseline.json` for pinned artifact fingerprints
- If making source changes, run `python3 -m py_compile` on changed files

---

*This handoff was created automatically at session start.*
