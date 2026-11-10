# Agentic Work Session Handoff

**Timestamp:** 2026-11-10T13:14:59Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

```bash
# Convention robustness check (~seconds)
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification (~8 min; 8 experiment drivers)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; +18 committed drivers)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Convention only (no writes)
SEED=42 python3 verify_convention_robustness.py
# or
make verify
```

## Key Integrity Notes

- **Golden artifacts**: `experiments/*.json` are canonical. Verification backs them up to `.verify_snapshot/` with `ACTIVE.json` marker (pid). Interrupted runs are recoverable via `python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- **Golden baseline**: `ledger/golden_baseline.json` pins SHA-256 of each artifact. `scripts/check_golden_baseline.py` guards against committed baseline replacement. Never re-pin as side effect of verification.
- **Data coverage**: `scripts/check_data_coverage.py` enforces all `data.download()` calls resolve to pinned cache files in `data/` matching `ledger/data_baseline.json`. Run with `--update` to add new inputs.
- **Optimizer determinism**: `src/portfolio_opt.py` validates solver answer on problem constraints, not exit status. Tangency QP is ill-conditioned (1-ulp input → ~1e-05 output drift). Do not re-pin E041/E042 grid artifacts.

## Next Steps / Open Items

See `ledger/RESEARCH_LEDGER.md` for:
- E049: Optimizer determinism fix (SLSQP status 8 handling)
- E045/E029: E029 fundamentals pinned for offline reproducibility
- E048: E030 panel committed, cache coverage enforced
- Open item: E041 remaining 133 numeric differences (1-ulp ill-conditioned QP) - do not re-pin

## Environment

- Python 3, dependencies in `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- cvxpy/cvxopt optional; falls back to scipy.optimize
- Seed: Always use `SEED=42` for reproducibility