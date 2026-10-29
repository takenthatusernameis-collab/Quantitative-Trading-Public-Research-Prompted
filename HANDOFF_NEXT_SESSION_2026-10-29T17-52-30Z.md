# Handoff for Next Agentic Work Session

**Created:** 2026-10-29T17:52:30Z
**Session Context:** Research phase complete (E001–E049). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Verification baseline integrity guards in place. Repository verified stable as of this handoff.

---

## Initial Task Message (START HERE)

> Repository is fully verified and in a stable state. **No new research is warranted.**
> Your primary task is to verify stability by running the extended verification suite,
> confirm the pre-existing known drifts remain unchanged, and report results.
> **Do not modify goldens, weaken tolerances, or change any gate logic.**
> If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
> All constraints from below still apply.

## Current State (verified at handoff time)

- **Branch:** `main`, up to date with `origin/main`. HEAD `0cc6b56` (chore(kilo): checkpoint agent session).
- **Working tree:** clean of tracked changes. Only `__pycache__/*.pyc` show as modified — these are tracked files with mtime drift (pyc header embeds mtime); no source, experiment, or ledger changes. Do not commit them.
- **No `.verify_snapshot/`** active; no untracked files; no stale verification output.
- **`experiments/*.json` goldens match HEAD.**
- **`SEED=42 bash scripts/check.sh` → ALL CHECKS PASSED** (goldens vs HEAD, stale-snapshot check, convention robustness, py_compile, data-coverage guard, golden-baseline fingerprint guard, template validation, experiment-script imports).
- **Research phase complete (E001–E049).** Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Latest committed work: **E049** (2026-10-20) — `src/portfolio_opt.py` solver-exit-status defect fixed, `tests/test_portfolio_opt.py` added, E042-lead artifact re-pinned. Research conclusions unchanged (E041 REJECTED, E042 PARTIAL).

## Precise Task (bounded, optional)

Re-run the verification suite to confirm stability:

```bash
SEED=42 python3 run_all_verification.py --extended
```

Expect the pre-existing E030/E041 drift below. **Do not** weaken tolerances, skip drivers, or modify committed goldens. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Known Pre-Existing Drift (reporting-only, decisions unchanged)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.
- **E041/E042 sensitivity grids and full E042 confirmatory golden** are not byte-reproducible in this sandbox: residual 1-ulp sensitivity of the ill-conditioned tangency QP in `src/portfolio_opt.py`. No structural differences; no gate or decision affected. Do NOT re-pin — see ledger E049.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).
- Do not commit `__pycache__/*.pyc` — they are tracked but drift by mtime only; leave them unstaged.

## Candidate Next Research Tasks (unstarted; pick one and pre-register)

Per the 2026-10-29T17:03 handoff, the highest-value unstarted task is:

**Optimize TSM+DN blend weights and evaluate adding a diversifier.**
- Grid search TSM/DN ratios (0/100, 25/75, 50/50, 75/25, 100/0), monthly rebal; evaluate Sharpe, beta vs SPY, turnover, MaxDD, bear-market performance.
- Success: Sharpe >= 1.65 or meaningfully lower MaxDD with |beta| < 0.2.
- Document as a new pre-registered experiment (E050+) in `ledger/RESEARCH_LEDGER.md` with gates and falsification expectations before running.
- Prerequisites: `src/backtest.py` custom weighting; strategies `time_series_momentum_pure` (src/strategies.py:153), `dollar_neutral_lowbeta` (src/strategies.py:278); data cached in `data/` (large_liquid).

## Prerequisites

- Dependencies installed (`pip install -r requirements.txt`: numpy, pandas, scipy, pyarrow, statsmodels, yfinance).
- Working tree clean; `SEED=42` for all verification commands.
- Cached 2026-10-12 parquet vintage in `data/`; E029 fundamentals snapshot pinned in `data/fundamentals/`.

## Key References

- `AGENTS.md` — commands, conventions, baseline integrity rules.
- `ledger/RESEARCH_LEDGER.md` — experiment history and disposition (E001–E049).
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `scripts/check.sh`, `run_all_verification.py`, `scripts/check_data_coverage.py`.
- `HANDOFF_REPRO_CAVEAT.md` — E041/E042 reproducibility caveat documentation.
- `HANDOFF_CURRENT.md` / `HANDOFF_NEXT_SESSION.md` — symlinks to the most recent handoff.