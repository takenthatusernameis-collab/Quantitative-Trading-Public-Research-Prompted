# Handoff for Next Agentic Work Session

**Created:** 2026-10-29T17:45:12Z
**Session Context:** Research phase complete (E001–E049). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Baseline integrity guards in place; repo is clean except pycache timestamps.

## Current State (verified at handoff time)

- `git status`: only `__pycache__/*.pyc` files show as modified (byte-identical sizes, mtime drift) — no source, experiment, or ledger changes.
- No `.verify_snapshot/` active; no untracked files; no stale verification output.
- `experiments/*.json` goldens match HEAD.
- Latest committed work: E049 (2026-10-20) — `src/portfolio_opt.py` solver-exit-status defect fixed, `tests/test_portfolio_opt.py` added, E042-lead artifact re-pinned. Research conclusions unchanged (E041 REJECTED, E042 PARTIAL).

## Initial Task (Start Here)

**Goal:** Establish a clean, verified baseline before making any changes.

### Steps

1. **Check repo state**
   ```bash
   git status --short && git log --oneline -3
   ```

2. **Run fast integrity checks**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - Validates goldens vs HEAD, stale-snapshot check, convention robustness, py_compile, data-coverage guard, golden-baseline fingerprint guard.
   - If it fails on golden/snapshot issues, follow the "Baseline Integrity" section in `AGENTS.md` before proceeding.

3. **Run quick verification (if checks pass)**
   ```bash
   SEED=42 python3 run_all_verification.py
   # or: make verify-quick
   ```
   - ~8 min; re-runs the 8-driver quick block (E012, E023, E024-merge, E027, E035, E037, E039, E042-lead) and restores canonical baselines.
   - **Do not commit** verification output. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

4. **Report status**
   - Summarize `check.sh` and `verify-quick` results.
   - Review `ledger/RESEARCH_LEDGER.md` open items (E049 residual ill-conditioning; E041/E042 grid drift of 29–133 numeric diffs).
   - Only proceed with new work after baseline is confirmed clean.

## Open Items (do not re-pin to silence)

- **E041/E042 sensitivity grids and full E042 confirmatory golden** are not byte-reproducible in this sandbox: residual 1-ulp sensitivity of the ill-conditioned tangency QP in `src/portfolio_opt.py`. 133 numeric diffs (E041), 56 (E042 min-var), 42 (E042 grid), 29 (E041 grid). No structural differences; no gate or decision affected. Do NOT re-pin — see ledger E049.
- **CI gate**: `.github/workflows/verification-gate.yml` still requires maintainer action via GitHub UI (agents cannot push workflows). Copyable template at `.github/workflow-templates/verification-gate.yml`; instructions in `VERIFICATION_GATE_TEMPLATE.md`.

## Candidate Next Research Tasks (unstarted; pick one and pre-register)

Per the 2026-10-29T17:03 handoff, the highest-value unstarted task is:

**Optimize TSM+DN blend weights and evaluate adding a diversifier.**
- Grid search TSM/DN ratios (0/100, 25/75, 50/50, 75/25, 100/0), monthly rebal; evaluate Sharpe, beta vs SPY, turnover, MaxDD, bear-market performance.
- Success: Sharpe >= 1.65 or meaningfully lower MaxDD with |beta| < 0.2.
- Document as a new pre-registered experiment (E050+) in `ledger/RESEARCH_LEDGER.md` with gates and falsification expectations before running.
- Prerequisites: `src/backtest.py` custom weighting; strategies `time_series_momentum_pure`, `dollar_neutral_lowbeta` in `src/strategies.py`; data cached in `data/` (large_liquid).

## Prerequisites

- Dependencies installed (`pip install -r requirements.txt`: numpy, pandas, scipy, pyarrow, statsmodels, yfinance).
- Working tree clean; `SEED=42` for all verification commands.
- Cached 2026-10-12 parquet vintage in `data/`; E029 fundamentals snapshot pinned in `data/fundamentals/`.

## Success Criteria

- `scripts/check.sh` passes with no golden/snapshot mismatches.
- `run_all_verification.py` (verify-quick) completes and restores `experiments/*.json` to committed baselines.
- No uncommitted modifications to tracked artifacts under `experiments/` from verification.
- Clear status summary documented before starting new work.

## Key References

- `AGENTS.md` — commands, conventions, baseline integrity rules.
- `ledger/RESEARCH_LEDGER.md` — experiment history and disposition (E001–E049).
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `scripts/check.sh`, `run_all_verification.py`, `scripts/check_data_coverage.py`.
- `HANDOFF_REPRO_CAVEAT.md` — E041/E042 reproducibility caveat documentation.