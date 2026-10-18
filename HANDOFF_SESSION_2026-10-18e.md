# Handoff: Extended verification completed (deps installed) + E041 structural diff documented

## What changed

No code, gate, decision, or validated construction was modified. Working
tree is clean except three documentation files recording the completed
verification:

- `HANDOFF_REPRO_CAVEAT.md` — corrected the prior session's overclaim. An
  earlier version stated "no structural/string differences" for
  `--extended`; that was **wrong** — it came from a run that timed out
  before reaching E019–E041 (see HANDOFF_SESSION_EXTENDED_BLOCKED.md:
  "e019-e041 unknown (timed out)"). The E041 row now reads "grid 361 diffs
  + 30 structural (8->7 market-neutral configs, boundary-crosser
  grid[11])", and the evidence block documents the boundary-crosser,
  same-seed determinism, and the snapshot/restore behaviour.
- `ledger/RESEARCH_LEDGER.md` — E041 Erratum 2 (reproducibility caveat,
  structural not just numeric).
- `README.md` — reproducibility section now states the E041 8/96 -> 7/96
  structural exception explicitly (it previously claimed the count
  "recomputes identically").

## What was actually verified (evidence)

Dependencies installed and match `requirements.txt` exactly (numpy 2.5.4,
pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0,
yfinance 1.7.0) on Python 3.12.3. The 2026-10-12 data vintage is cached.

- `SEED=42 bash scripts/check.sh` -> `=== All checks passed ===` (107/107
  committed JSON artifacts parse; convention robustness 15 strategies; all
  27 experiment scripts import OK).
- `SEED=42 python3 run_all_verification.py --extended` -> **FAILURES
  DETECTED**. The suite ran to completion (all 18 extended drivers + 8 quick
  drivers + batch_run + validate + E042 quick). Snapshot/restore worked: the
  18 modified goldens were restored from the backup and `git status` is clean.
  - 25 of 26 drivers pass (exact or bounded-float match).
  - **1 failure: `run_e041.py`** — 30 structural mismatches across
    `experiments/e041_market_neutral_portfolio.json` and
    `experiments/e041_sensitivity_grid.json` (8 -> 7 market-neutral configs;
    `top_configs[6]` method `max_sharpe` -> `risk_parity`, beta 0.1 -> 0.15,
    turnover 0.0099 -> 0.0080), plus ~361 grid / ~9089 main numeric diffs.
- **E041 root cause isolated**: grid config index 11
  (`max_sharpe, beta<=0.1, macro_inclusive_3`) is a boundary-crosser —
  OOS Sharpe 0.8156 in the committed golden (clears >= 0.8) vs 0.7578 fresh
  (fails), while equity beta 0.025 sits inside the |beta| <= 0.1 bar in
  both. The SLSQP walk-forward optimizer in `src/portfolio_opt.py` shifts it
  across the 0.8 threshold.
- **E041 determinism confirmed**: two full `SEED=42 run_e041.py`
  executions agree to 0 diffs (grid and main), so this is environment drift
  vs the committed baseline, not non-determinism.
- **No gate or decision impact**: E041 stays REJECTED (3/5, G3
  market-neutrality fails on the primary max_sharpe portfolio regardless
  of the grid count). E042 stays PARTIAL (4/5, G2 fails).
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

- Regenerating the E041/E042 goldens from the current code: the fresh output
  is internally consistent and deterministic across same-seed runs, but it
  would replace the committed baseline with environment-specific numbers,
  breaking cross-artifact consistency (the E042 grid would no longer match
  the E042b lead golden). Prohibited and would destroy the grid's role as
  the ground-truth record.
- Weakening `numeric_tol` or skipping drivers: prohibited by task
  constraints.
- Claiming the goldens reproduce exactly: disproven by direct measurement
  (25/26 drivers match or drift within tolerance; E041 has 361 grid + 30
  structural diffs and ~9089 main diffs).
- Claiming E041 has "no structural differences": disproven by the complete
  `--extended` run (the prior session never finished it). Corrected in the
  docs.

## One precise next task

The repository is in a clean, documented state. The only remaining durable
action outside agent scope is the maintainer-gated CI workflow creation
(template at `.github/workflow-templates/verification-gate.yml`). If a
bounded in-session task is desired, the lowest-risk option is to re-run
`SEED=42 bash scripts/check.sh` and confirm `git diff` contains only the
three documentation files above.

### Constraints
- Do NOT modify committed goldens; rely on `run_all_verification.py`'s
  backup/restore mechanism.
- Honor `SEED=42` and the cached 2026-10-12 parquet vintage.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or
  validated constructions (`src/backtest.py`, `src/strategies.py`,
  `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- Do not weaken comparison tolerances or skip drivers to make the suite pass.