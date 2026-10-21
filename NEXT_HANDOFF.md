# Next Task: Re-run extended verification after E031 fix

## Context
This session fixed the only malformed committed artifact in the repo
(`experiments/e031_accruals_feasibility.json`: stray `]` -> `}`) and added
`scripts/check_json_artifacts.py` as the first fast check in
`scripts/check.sh`. The fast offline suite passes (`SEED=42 bash scripts/check.sh`
-> `=== All checks passed ===`, 107/107 committed JSON artifacts parse).

The pinned scientific dependencies were **not** installed in this sandbox
(`ModuleNotFoundError: numpy`), so the slow verification suite could not be
executed. That is the open item.

## Precise task
1. `pip install -r requirements.txt` (pinned versions; Python 3.12.3 is present).
2. Run `SEED=42 python3 run_all_verification.py --extended` (~21 min; re-executes
   all 26 committed experiment drivers + batch_run + validate + E042 quick).
3. Confirm **ALL CHECKS PASSED** and that `git status` is clean afterward
   (the suite backs up and restores `experiments/*.json`).

## Why this is the right next task
- It is the authoritative check. The fast offline path (AST/import/JSON-parse)
  cannot exercise any computation, so it cannot confirm the E031 fix introduced
  no regression in the suite that consumes experiment artifacts.
- It re-validates the entire committed baseline under the pinned dependencies,
  which is the repo's reproducibility claim.
- It is bounded, deterministic (SEED=42, cached 2026-10-12 vintage), and requires
  no new research, no gate changes, and no modification of validated constructions.

## Constraints
- Do NOT modify committed goldens; rely on `run_all_verification.py`'s
  backup/restore mechanism.
- Honor `SEED=42` and the cached parquet vintage (`data/vintages.json`,
  `default_end_date: 2026-10-12`).
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or
  validated constructions (`src/backtest.py`, `src/strategies.py`,
  `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- If `pip install` fails or the suite fails on a driver, record the evidence
  verbatim and do not weaken comparison tolerances or skip drivers to make it
  pass.

## Evidence already gathered
- `SEED=42 bash scripts/check.sh` -> exit 0 (convention robustness 15 strategies
  + 8 E024 decompositions + E042 gates + template validation + import guard +
  **107/107 committed JSON artifacts parse**).
- Guard negative test: corrupting a tracked artifact in place -> guard returns
  rc=1 and names the bad file; untracked files are not flagged.
- `git diff` shows the E031 change is exactly one bracket; no goldens touched,
  no `src/*` modified.
