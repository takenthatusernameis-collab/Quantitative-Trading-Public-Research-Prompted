# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-31T20:39:40Z (UTC)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `c139510` (HEAD; checkpoint commit)
**Working tree:** clean (no source/data changes pending)
**Snapshot state:** `.verify_snapshot/` does **NOT** exist — no recovery needed.

This session left a durable initial task message for the next agentic work session.
No source changes were made and no verification run was executed.

## INITIAL TASK (START HERE)

**Baseline integrity first, then address the standing E049 follow-up (tangency QP
ill-conditioning) so E041/E042 grid artifacts reproduce within tolerance without
reintroducing solver-status dependence.**

## Concrete Next Steps

1. **Confirm clean baseline:** `SEED=42 bash scripts/check.sh` — expect exit 0.
   - Covers `check_goldens_clean.py`, `check_golden_baseline.py`, `py_compile`, `test_portfolio_opt.py`, `check_data_coverage.py`.
2. **Confirm tree state:** `git status --short` — clean / only `__pycache__/*.pyc` allowed.
3. **Quick verification:** `SEED=42 python3 run_all_verification.py --skip-slow` (~8 min).
   - Never leave the run half-finished; do not commit verification outputs.
4. **Investigate well-conditioned solver for small N (<=5 assets):** exact KKT
   enumeration as reference; CVXOPT/OSQP/custom active-set as stable alternative;
   preserve feasibility-validation invariant (`src/portfolio_opt.py`).
5. **Validate:** run E041/E042 lead drivers offline with `SEED=42 QUANT_RESEARCH_OFFLINE=1`.
6. **Document findings:** update `ledger/RESEARCH_LEDGER.md`; re-pin goldens only
   via `python3 scripts/check_golden_baseline.py --update` with rationale.

## Environment State (verified this session)

- `SEED=42 bash scripts/check.sh` -> `=== All checks passed ===` (exit 0).
  Requires `pip install -r requirements.txt` first (`/usr/bin/python3` 3.12.3 had no
  pandas/numpy/scipy; `pip3 install --break-system-packages -r requirements.txt`
  yields numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels
  0.15.0, yfinance 1.7.0). Re-install if the next session's environment is reset.
- Data caches in `data/` are present and git-tracked (2026-10-12 and 2026-10-11
  vintages). `data/panel.parquet` does **not** exist and is not referenced by any
  tracked baseline; `check.sh` passes without it.
- No `.verify_snapshot/` is pending. No recovery needed.

## Constraints (Do Not Violate)

- Always use `SEED=42`. Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`).
- Never leave `run_all_verification.py` half-finished.
- Do not re-pin goldens without ledger justification.
- Do not commit verification outputs; only intentional source/data changes.
- Honor "judge answer on problem constraints, not solver status" invariant.

## References

- `AGENTS.md` — commands, guards, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — decisions, gates, open items (notably E041/E042
  optimizer drift and cache coverage enforcement)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `run_all_verification.py`, `scripts/check.sh`, `scripts/check_goldens_clean.py`,
  `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`

## Session Summary

This session created a durable handoff only; no source/data changes and no
verification run executed. Working tree remains clean at HEAD `c139510`.
