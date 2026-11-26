# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T08:21:41Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Workspace Root**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover the golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Files to Review

- `AGENTS.md` - Project commands, conventions, and verification procedures
- `ledger/RESEARCH_LEDGER.md` - Documented surviving validated strategies (E001–E043)
- `scripts/check.sh` - Fast convention-robustness check
- `run_all_verification.py` - Main verification suite
- `experiments/*.json` - Canonical research artifacts (golden files)

## Baseline Integrity Notes

- `experiments/*.json` are canonical research artifacts
- Verification suite overwrites them while re-running and restores afterward
- **Never leave a verification run half-finished** - it must complete or be restored
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard baseline integrity

## Reproducibility Requirements

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Cache coverage**: Enforced invariant - all `data.download()` calls must have pinned cache files
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Next Session Suggested Starting Points

1. Run `SEED=42 bash scripts/check.sh` to verify environment health
2. Check `ledger/RESEARCH_LEDGER.md` for current research status
3. Consider running `SEED=42 python3 run_all_verification.py --skip-slow` for quick validation
4. Review any open items in the ledger for potential follow-up experiments

---

*This handoff was created automatically at session start for the next agentic work session.*