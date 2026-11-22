# Handoff Message — 2026-11-22T22:54:38Z

## Project State
- **Repository**: Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Current baseline**: Golden artifacts in `experiments/*.json` are canonical. Verification suite overwrites and restores them.

## Quick Commands
```bash
# Convention robustness check (seconds, offline)
SEED=42 bash scripts/check.sh
# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# Full verification (~15 min + 50 sims)
SEED=42 python3 run_all_verification.py --full
```

## Key Invariants
- **Seed**: Always `SEED=42` for reproducibility.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage enforced by `scripts/check_data_coverage.py`.
- **Golden files**: Never commit verification output. If interrupted, run `run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- **Optimizer determinism**: SLSQP status 8 is acceptable at constrained optimum (validated by `tests/test_portfolio_opt.py`). Ill-conditioned QP causes 1-ulp drift in E041/E042 grid artifacts — do not re-pin to silence.

## Open Items (from ledger)
- E041: 133 numeric differences remain post-fix (ill-conditioned QP). Open item — do not re-pin.
- E030: Now offline-reproducible (pinned 16-ETF panel), 0 diffs since 2026-10-20.
- E029: Offline-reproducible (pinned fundamentals snapshot), 0 diffs.

## Next Session Suggestions
1. Run `make check` to validate conventions and golden baseline integrity.
2. If clean, run `make verify-quick` for fast regression.
3. Review `ledger/RESEARCH_LEDGER.md` for promotion candidates requiring confirmatory runs.
4. Any new experiment: pre-register with gates, falsification expectations, and sensitivity grid before execution.

## Files to Watch
- `ledger/golden_baseline.json` — SHA-256 pins for all `experiments/*.json`
- `ledger/data_baseline.json` — SHA-256 pins for all cached data inputs
- `data/vintages.json` — 2026-10-12 vintage pin
- `data/fundamentals_vintages.json` — E029 fundamentals pin
- `src/portfolio_opt.py` — optimizer determinism logic
- `tests/test_portfolio_opt.py` — validates optimizer acceptance rule