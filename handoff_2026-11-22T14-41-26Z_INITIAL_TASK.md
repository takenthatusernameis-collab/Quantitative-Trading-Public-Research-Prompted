# Agentic Work Session Handoff

**Created:** 2026-11-22T14:41:26Z
**Status:** Initial task message — pending next agentic work session

## Task

No specific task defined yet. This file is the durable handoff marker for the next agentic work session in `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`.

## Repository context

- Quantitative-strategy research repo on 2014–2026 US equities, futures, macro data.
- Research phase complete (E001–E043); strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` (committed goldens). Verification re-runs drivers and restores them — never leave a run half-finished.
- Key commands:
  - `SEED=42 bash scripts/check.sh` — convention-robustness check + template validation (fast, offline)
  - `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min)
  - `SEED=42 python3 run_all_verification.py --extended` / `--full` / `--skip-slow`
  - `SEED=42 python3 run_all_verification.py --restore-only` — recover goldens after interrupted run
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).
- `cvxpy`/`cvxopt` optional; portfolio optimizer falls back to `scipy.optimize`.
- Cache coverage invariant: `scripts/check_data_coverage.py` — every `data.download()` call site must have a git-tracked cache file matching `ledger/data_baseline.json`. Offline mode `QUANT_RESEARCH_OFFLINE=1`.
- Lint: `python3 -m py_compile` on changed files (no separate linter).

## Open items (from AGENTS.md ledger)

- E041 remaining 133 numeric differences (1-ulp QP sensitivity) still exceed 1e-4 tolerance — do NOT re-pin to silence. See ledger open item.
- E042 tangency portfolio solver determinism (SLSQP status 8 at constrained optimum) — gating on solver exit status made artifacts environment-dependent; fixed in `src/portfolio_opt.py` per `tests/test_portfolio_opt.py`.

## Next step

Define the actual task for the next session, then execute it. Do not commit unless explicitly asked. Restore goldens (`--restore-only`) before committing if a verification run was interrupted.
