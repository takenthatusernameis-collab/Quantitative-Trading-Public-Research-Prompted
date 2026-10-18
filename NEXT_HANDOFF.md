# Next Task: None remaining in agent scope — repo is clean and documented

## Context

This session executed the prior handoff: installed the pinned dependencies
(`pip install -r requirements.txt` -> numpy 2.5.4, pandas 3.0.6, scipy
1.18.1, pyarrow 26.0.0, statsmodels 0.15.0, yfinance 1.7.0 on Python 3.12.3)
and ran `SEED=42 python3 run_all_verification.py --extended` to completion
(all 26 committed drivers + batch_run + validate + E042 quick). The suite's
snapshot/restore mechanism worked: `git status` is clean.

Result: **25 of 26 drivers pass** (exact or bounded-float match). **One
failure: `run_e041.py`** — a genuine structural diff, not numeric drift.

## Finding: E041 has a structural diff (8 -> 7 market-neutral configs)

The prior session's reproducibility caveat claimed "no structural/string
differences" for `--extended`. That claim was **wrong**: it came from a run
that timed out before reaching E019–E041 (HANDOFF_SESSION_EXTENDED_BLOCKED.md:
"e019-e041 unknown (timed out)"), so E041 was never actually compared. The
complete run corrects this.

Root cause: grid config index 11 (`max_sharpe, beta<=0.1,
macro_inclusive_3`) is a **boundary-crosser** — its OOS Sharpe is **0.8156**
in the committed `experiments/e041_sensitivity_grid.json` (clears the >= 0.8
gate, so it is counted in the **8/96**) vs **0.7578** in a fresh run (fails
the gate, so the count drops to **7/96**). Its equity beta (0.025) sits well
inside the |beta| <= 0.1 bar in both, so only the Sharpe threshold is
crossed. The SLSQP walk-forward optimizer in `src/portfolio_opt.py` shifts
it across the 0.8 boundary, which also changes the `top_configs` list length
(8 -> 7) and the trailing entry's method (`max_sharpe` -> `risk_parity`),
beta_constraint (0.1 -> 0.15), and turnover (0.0099 -> 0.0080).

**Determinism confirmed**: two full `SEED=42 run_e041.py` executions agree
to 0 diffs (grid and main), so this is environment drift vs the committed
baseline, not non-determinism. **No gate or decision is affected**: E041
stays REJECTED (3/5, G3 market-neutrality fails on the primary max_sharpe
portfolio regardless of the grid count).

## What was verified

- `SEED=42 bash scripts/check.sh` -> `=== All checks passed ===` (107/107
  committed JSON artifacts parse; convention robustness 15 strategies; all
  27 experiment scripts import OK).
- `SEED=42 python3 run_all_verification.py --extended` -> FAILURES
  DETECTED (1 of 26 drivers: E041, structural). Snapshot/restore worked;
  `git status` clean.
- E041 root cause isolated to the boundary-crosser above; determinism
  confirmed by two same-seed runs.
- `python3 -m py_compile scripts/check_json_artifacts.py
  verify_convention_robustness.py run_all_verification.py` -> OK.

## What remains unresolved

- The `--extended` suite fails on E041 (structural, boundary-crosser) in
  this sandbox. The committed E041 goldens are retained as authoritative
  (8/96); regenerating them from the current code would produce 7/96 and
  break cross-artifact consistency with the E042 grid. Prohibited by the
  "do not modify committed goldens" constraint.
- CI gate workflow (`.github/workflows/verification-gate.yml`) still
  requires maintainer action (GitHub UI) — automated agents cannot push
  workflows.

## Which approaches have already failed and why

- Regenerating the E041/E042 goldens from the current code: prohibited and
  would destroy cross-artifact consistency.
- Weakening `numeric_tol` or skipping drivers: prohibited by task
  constraints.
- Claiming the goldens reproduce exactly: disproven by direct measurement.
- Claiming E041 has "no structural differences": disproven by the complete
  `--extended` run; corrected in the docs.

## One precise next task

No bounded, high-value task remains within agent scope. The repository is
in a clean, documented state. The only durable action outside agent scope
is the maintainer-gated CI workflow creation (template at
`.github/workflow-templates/verification-gate.yml`).

If a bounded in-session task is still desired, the lowest-risk option is to
re-run `SEED=42 bash scripts/check.sh` and confirm `git diff` contains only
the three documentation files (`HANDOFF_REPRO_CAVEAT.md`,
`ledger/RESEARCH_LEDGER.md`, `README.md`, plus this file).

### Constraints
- Do NOT modify committed goldens; rely on `run_all_verification.py`'s
  backup/restore mechanism.
- Honor `SEED=42` and the cached 2026-10-12 parquet vintage.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or
  validated constructions (`src/backtest.py`, `src/strategies.py`,
  `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- Do not weaken comparison tolerances or skip drivers to make the suite pass.