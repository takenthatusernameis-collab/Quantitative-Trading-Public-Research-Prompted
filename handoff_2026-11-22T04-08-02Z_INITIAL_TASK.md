# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-22T04:08:17Z
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Research Phase:** Complete (E001–E043)
**Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `SEED=42 bash scripts/check.sh` | Fast convention-robustness + template validation (~seconds) |
| `SEED=42 python3 run_all_verification.py` | Quick full verification (~8 min) |
| `SEED=42 python3 run_all_verification.py --extended` | Extended verification (~21 min) |
| `SEED=42 python3 run_all_verification.py --full` | Full verification (~15 min, n_sim=50) |
| `SEED=42 python3 run_all_verification.py --restore-only` | Restore golden artifacts after interrupted run |

## Critical Baseline Integrity Notes

- **Golden files:** `experiments/*.json` are canonical artifacts. Verification overwrites and restores them.
- **Never leave a verification run half-finished** — it corrupts the baseline.
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Golden baseline guard:** `scripts/check_golden_baseline.py` compares tracked artifacts to SHA-256 in `ledger/golden_baseline.json`. Re-pinning requires explicit `--update` and shows in diff.
- **Data coverage invariant:** `scripts/check_data_coverage.py` enforces every `data.download()` call site has a committed, SHA-256-pinned cache file (see `ledger/data_baseline.json`).

## Reproducibility Requirements

- **Seed:** Always `SEED=42` (walk-forward + placebo RNG)
- **Convention:** Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Dependencies:** `pip install -r requirements.txt` (cvxpy/cvxopt optional)

## Known Drift Items (Ledger E045, E048, E049)

- **E029, E030:** Now offline-reproducible (pinned fundamentals + 16-ETF panel), 0 diffs
- **E041:** 133 numeric diffs (1-ulp ill-conditioned QP), 0 structural — **do not re-pin**
- **E042 grid artifacts:** 29–133 numeric diffs from same QP ill-conditioning — **do not re-pin**
- **Optimizer rule:** `src/portfolio_opt.py` validates on problem constraints, NOT solver exit status (tested in `tests/test_portfolio_opt.py`)

## Next Steps / Open Items

1. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open dispositions
2. Decide on promotion path for any PARTIAL results requiring confirmatory runs
3. Consider CI gate setup (template at `.github/workflow-templates/verification-gate.yml`)

---

*This handoff was created automatically. Update as needed before committing.*