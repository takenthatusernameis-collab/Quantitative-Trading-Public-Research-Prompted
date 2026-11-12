# Agentic Work Session Handoff

**Timestamp:** 2026-11-12T22:01:25Z
**Session ID:** Initial handoff created at user request
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

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

## Key Files & Directories

- `experiments/*.json` - Canonical research artifacts (golden baselines)
- `ledger/RESEARCH_LEDGER.md` - Documented surviving validated strategies
- `ledger/golden_baseline.json` - SHA-256 fingerprints of golden artifacts
- `ledger/data_baseline.json` - SHA-256 fingerprints of pinned data cache
- `src/` - Core research code (batch_run.py, validate.py, portfolio_opt.py, etc.)
- `scripts/` - Verification and validation scripts
- `data/` - Cached parquet data (gitignored except pinned vintages)
- `tests/` - Unit tests (e.g., test_portfolio_opt.py)

## Critical Conventions

1. **Always use `SEED=42`** for reproducibility (walk-forward + placebo RNG)
2. **Golden files are sacred** - verification suite backs them up before re-running and restores after
3. **Never commit verification output** - if interrupted, restore with `run_all_verification.py --restore-only` or `git checkout -- experiments/`
4. **Cache coverage is enforced** - all data downloads must be pinned via `scripts/check_data_coverage.py --update`
5. **Pre-registration is mandatory** - every experiment has falsification expectations documented before execution

## Verification Suite Behavior

- `verify-quick`: Re-executes 8 drivers (E012, E023, E024, E027, E035, E037, E039, E042-lead)
- `verify-extended`: Adds 18 more drivers, compares to committed goldens (numeric_tol=1e-4)
- `verify-full`: Full E042 n_sim=50 + 96-config sensitivity grid
- Reports written to `.verify_reports/` (gitignored, never contaminates baseline)

## Known Drift Items (as of 2026-10-20)

- **E030**: 28 numeric diffs on near-zero quantities (reproduces with 0 diffs since 2026-10-20 after panel commit)
- **E041**: 133 numeric diffs (1-ulp sensitivity of ill-conditioned QP), 3 structural diffs resolved. **Do not re-pin** - see ledger open item.
- **E042 grid artifacts**: 29-133 differences from same ill-conditioned QP issue.

## Dependencies

```bash
pip install -r requirements.txt  # numpy, pandas, scipy, pyarrow, statsmodels, yfinance
# cvxpy/cvxopt optional - falls back to scipy.optimize
```

---

## Next Session Guidance

This handoff provides full context to resume work. The project is in a verified state with all golden baselines intact. Before making changes:

1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Any new experiment must follow pre-registration protocol
4. Data additions require cache pinning via `scripts/check_data_coverage.py --update`

**No pending tasks or blockers at handoff time.**