# Handoff: Fix `deterministic_timestamp()` NameError in experiment drivers

## What changed
Commit `a03264a` (prior agent) replaced non-deterministic timestamps
(`datetime.utcnow()`) with `deterministic_timestamp()` calls in 5 experiment
drivers, but did **not** import the helper (defined in `src/run_experiment.py:81`).
Re-running any of them raised `NameError: name 'deterministic_timestamp' is not
defined`, breaking the repo's reproducibility claim for those drivers.

Fix applied (5 files, one import line each):
- `experiments/run_e012.py`: `from src.run_experiment import UNIVERSES` ->
  `from src.run_experiment import UNIVERSES, deterministic_timestamp`
- `experiments/run_e023.py`: added `from src.run_experiment import deterministic_timestamp`
- `experiments/run_e024.py`: added `deterministic_timestamp` to the existing `src.run_experiment` import
- `experiments/run_e027.py`: added `from src.run_experiment import deterministic_timestamp`
- `experiments/run_e035.py`: added `from src.run_experiment import deterministic_timestamp`

Regression guard added (fast, offline, AST-based — no execution/data):
- `scripts/check_experiment_imports.py` (new): asserts every `experiments/run_e*.py`
  that calls `deterministic_timestamp()` imports it from `src.run_experiment`.
- Wired into `scripts/check.sh` (no other changes to it).

## What was actually verified (evidence)
- Bug reproduced BEFORE fix: `SEED=42 python3 experiments/run_e027.py` ->
  `NameError: name 'deterministic_timestamp' is not defined` (exit 1) at line 207.
- `python3 -m py_compile` OK on all 5 files (and all `experiments/run_e*.py`).
- Import resolves at module load for run_e012/run_e023/run_e027/run_e035
  (`__import__` + `hasattr(m, 'deterministic_timestamp')` = True).
- `deterministic_timestamp()` under `SEED=42` returns the pinned-vintage value
  `"2026-10-12T00:00:00Z"` (matches `data/vintages.json` default date).
- End-to-end re-run AFTER fix: `SEED=42 python3 experiments/run_e027.py` -> exit 0
  (golden backed up to /tmp and restored afterward; `git status` clean).
- `SEED=42 python3 experiments/run_e024.py --merge` -> exit 0. `--merge` mode calls
  `_merge()` which invokes `deterministic_timestamp()` at line 765, so this
  exercises the fixed call site without the ~15-min full audit
  (golden backed up/restored; `git status` clean).
- Guard negative-test: an AST-reconstructed "calls but not imported" script is
  flagged `would_fail=True` -> guard genuinely detects the original bug.
- `SEED=42 bash scripts/check.sh` -> `=== All checks passed ===`, exit 0
  (verify_convention_robustness.py + validate_template.py + check_experiment_imports.py).

## What remains unresolved
- The 5 committed golden JSONs (`e012_market_neutral.json`, `e023_economic_trend.json`,
  `e024_convention_audit.json`, `e027_ivol_anomaly.json`, `e035_illiquidity.json`)
  still carry the ORIGINAL non-deterministic timestamps (e.g.
  `e027_ivol_anomaly.json` = `2026-10-12T03:58:54.147534Z`). They were NOT regenerated,
  per the prior constraint "do not regenerate experiment goldens". Numbers are
  unaffected and verification strips `timestamp` during comparison, but the timestamp
  field is now stale relative to the deterministic-timestamp behavior. Regenerating
  is explicitly out of scope for this session.
- `run_e024.py` full normal-mode run was NOT executed (too slow); only `--merge` was
  used to exercise the timestamp call site. Numbers are unchanged by the import fix.
- The CI gate workflow (`.github/workflows/verification-gate.yml`) remains a
  maintainer-only, GitHub-UI task (token lacks `workflows` permission; controller
  resets `.github/workflows`). Unchanged by this session.

## Which approaches have already failed and why
- Directly importing `experiments.run_e024` as a module fails with
  `ModuleNotFoundError: No module named 'run_e017'` (no `experiments/__init__.py`;
  `from experiments.run_e017 import` only resolves when run as a script). This is
  PRE-EXISTING and unrelated to the `deterministic_timestamp` fix; the AST guard
  (which parses source, not imports) is used instead of module-import checks
  precisely to avoid this false signal.

## One precise next task (evidence + constraints)
Extend `run_all_verification.py` (quick mode) to re-execute the five experiment
drivers E012/E023/E024/E027/E035 and assert their fresh output matches the committed
goldens with the `timestamp` field stripped — using the existing `snapshot`/`restore`
+ `compare_patterns` helpers so committed goldens are never permanently overwritten.

Evidence this is sound:
- All 5 drivers now run without `NameError` (verified above).
- `verify_convention_robustness.py` already asserts specific deterministic numbers
  from these goldens match, so the underlying computations are verified reproducible
  under `SEED=42` + cached data (vintage 2026-10-12).
- `run_all_verification.py` already backs up `experiments/*.json` to a temp dir and
  restores it in a `finally` block (lines 222-300), so overwriting goldens mid-run is
  already handled.

Constraints:
- Do NOT modify committed goldens; rely on the existing backup/restore mechanism.
- Honor `SEED=42` and cached parquet (calendar-independent via `data/vintages.json`).
- Add the 5 drivers ONLY to quick mode (keep `--full` as-is) to bound runtime; full
  E042 reproduction already dominates `--full`.
- Do not touch `.github/workflows/*` or core research logic.
