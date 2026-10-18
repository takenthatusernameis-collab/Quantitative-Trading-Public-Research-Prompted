# Session Handoff: Schema guard negative-test coverage added

## What changed
- Extended `tests/test_json_guard.py` from 5 → **19 tests**, covering every
  schema class in `scripts/check_json_artifacts.py` (EXPERIMENT_DRIVER,
  EXPERIMENT_ID_DRIVER, DATA_INFEASIBILITY, SENSITIVITY_GRID, STRATEGY_EVAL,
  E024_PART, NON_EXPERIMENT) plus malformed JSON, missing identifier, unknown
  structure, non-allowlisted top-level list, and an untracked-file smoke test.
  Each class has a positive (passes) and one or more negative (fails) case.
- Wired the suite into the fast offline path: `scripts/check.sh` now runs
  `python3 -m unittest tests.test_json_guard` between the artifact guard and
  convention robustness; `run_all_verification.py` gained step `[0.5b/4]`
  immediately after the artifact guard, aborting on failure.

## What was actually verified (evidence)
- `python3 -m unittest tests.test_json_guard -v` → **Ran 19 tests, OK** (exit 0).
- `SEED=42 bash scripts/check.sh` → **=== All checks passed ===** (exit 0);
  the suite output shows `Ran 19 tests ... OK` between the artifact guard and
  convention robustness.
- `python3 scripts/check_json_artifacts.py` → **107/107 committed JSON artifacts
  parse OK** (no goldens touched).
- `python3 -m py_compile run_all_verification.py tests/test_json_guard.py` → OK.
- `git status --short` → only `run_all_verification.py`, `scripts/check.sh`,
  `tests/test_json_guard.py` modified. No `experiments/*.json`, no `src/*`.

## What remains unresolved
- Scientific dependencies (numpy/pandas/scipy/statsmodels/pyarrow/yfinance)
  are not installed in this sandbox, so `run_all_verification.py --skip-slow`
  cannot complete: it crashes at `data_cache_ok()` (line 428) with
  `ModuleNotFoundError: No module named 'pandas'`. This is environmental, not a
  code regression — the fast offline path (check.sh) is the authoritative check
  here and passes. Installing `requirements.txt` and re-running
  `--skip-slow` (or `--extended`) is the obvious next step if the sandbox allows.
- CI workflow `.github/workflows/verification-gate.yml` still requires maintainer
  creation via GitHub UI (automated agents cannot push workflows).

## Which approaches have already failed and why
- Two of my first-pass test assertions were too specific: I asserted the guard
  would emit `SENSITIVITY_GRID missing required field 'grid'` for an artifact
  carrying `experiment` + `n_configs` but no `grid`. The guard's `classify()`
  requires **both** `grid` and `n_configs` to identify the class, so such an
  artifact is rejected earlier as `unrecognized artifact structure`. I corrected
  the assertions to match the guard's actual behavior rather than weakening the
  guard. No guard code was changed.
- The slow verification suite could not be executed in this sandbox (missing
  pandas); I did not weaken tolerances or skip steps to paper over that.

## One precise next task (bounded, high-value)
**Task: Install `requirements.txt` and run `SEED=42 python3 run_all_verification.py --skip-slow`.**
- This is the authoritative check that exercises the new step `[0.5b/4]` inside
  the real suite (rather than only via `check.sh`), and re-validates the whole
  committed baseline under pinned dependencies.
- If `pip install` is blocked, the fallback is to confirm the fast path remains
  green (`SEED=42 bash scripts/check.sh`) — already done, exit 0.

### Constraints
- Do not modify committed golden JSONs; rely on `run_all_verification.py`'s
  backup/restore mechanism.
- Honor `SEED=42` and the cached 2026-10-12 parquet vintage.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or
  validated constructions (`src/backtest.py`, `src/strategies.py`,
  `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).

(End of file - total 59 lines)