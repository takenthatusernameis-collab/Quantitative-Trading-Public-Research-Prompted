# Agentic Work Session Handoff

**Timestamp:** 2026-11-11T09:18:01Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Verification Commands Available

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

## Key Artifacts

- **Golden files:** `experiments/*.json` (canonical research artifacts, git-tracked)
- **Data cache:** `data/` (parquet, gitignored except pinned vintages 2026-10-12, 2026-10-11)
- **Fundamentals snapshot:** `data/fundamentals/` (pinned per `data/fundamentals_vintages.json`)
- **Ledger:** `ledger/RESEARCH_LEDGER.md` (surviving strategies, dispositions)
- **Data baseline:** `ledger/data_baseline.json` (SHA-256 pins for cache files)
- **Golden baseline:** `ledger/golden_baseline.json` (SHA-256 pins for experiment artifacts)

## Critical Integrity Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. Use `--restore-only` to recover if interrupted.
2. **Golden baseline protection** — `scripts/check_golden_baseline.py` compares artifacts against pinned SHA-256s. Re-pinning requires explicit `--update` and shows in diff.
3. **Cache coverage invariant** — `scripts/check_data_coverage.py` enforces all driver data inputs are pinned. Unpinned = live download = non-reproducible.
4. **E041 known drift** — 133 numeric differences (1-ulp ill-conditioned QP), 3 structural diffs fixed. Do not re-pin to silence; see ledger open item.
5. **Optimizer rule** — `src/portfolio_opt.py` validates on constraints, not solver exit status (tested in `tests/test_portfolio_opt.py`).

## Next Session Suggested Actions

- Run `make check` to verify baseline integrity before any changes
- Run `make verify-quick` for fast regression check
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
- Any new experiment requires pre-registration with falsification expectations and sensitivity grid

## Reproducibility Requirements

- Always use `SEED=42`
- Set `QUANT_RESEARCH_OFFLINE=1` for verification runs
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- Optional: cvxpy/cvxopt (falls back to scipy.optimize)

---
*This handoff was created automatically at session start for continuity across agentic work sessions.*