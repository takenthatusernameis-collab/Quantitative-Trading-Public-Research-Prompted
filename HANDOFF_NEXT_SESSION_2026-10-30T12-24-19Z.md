# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-30T12:24:19Z (UTC)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ HEAD
**Working tree:** clean except `__pycache__/*.pyc` (no source/data changes pending).
**Snapshot state:** `.verify_snapshot/` does **NOT** exist — no recovery needed.

This session left a durable initial task message for the next agentic work session.
No source changes were made and no verification run was executed.

## INITIAL TASK (START HERE)

**Baseline integrity first, then address the standing E049 follow-up (tangency QP
ill-conditioning) so E041/E042 grid artifacts reproduce within tolerance without
reintroducing solver-status dependence.**

## Concrete Next Steps

1. **Confirm clean baseline:** `SEED=42 bash scripts/check.sh` — expect exit 0.
2. **Confirm tree state:** `git status --short` — clean / only `__pycache__/*.pyc` allowed.
3. **Quick verification:** `SEED=42 python3 run_all_verification.py --skip-slow`.
4. **Investigate well-conditioned solver for small N (<=5 assets):** exact KKT
   enumeration as reference; CVXOPT/OSQP/custom active-set as stable alternative;
   preserve feasibility-validation invariant.
5. **Validate:** run E041/E042 lead drivers offline with `SEED=42 QUANT_RESEARCH_OFFLINE=1`.
6. **Document findings:** update `ledger/RESEARCH_LEDGER.md`; re-pin goldens only
   via `scripts/check_golden_baseline.py --update` with rationale.

## Environment State (verified this session)

- `SEED=42 bash scripts/check.sh` -> `=== All checks passed ===` (exit 0). This
  required installing `requirements.txt` first: the sandbox's `/usr/bin/python3`
  (3.12.3) had **no pandas/numpy/scipy**. `pip3 install --break-system-packages
  -r requirements.txt` now yields numpy 2.5.4, pandas 3.0.6, scipy 1.18.1,
  pyarrow 26.0.0, statsmodels 0.15.0, yfinance 1.7.0. If the next session's
  environment is reset, re-run that install before anything else.
- Data caches in `data/` are present and git-tracked (2026-10-12 and 2026-10-11
  vintages per `.gitignore` exceptions). `data/panel.parquet` does **not** exist
  and is not referenced by any tracked baseline; `check.sh` passes without it.
