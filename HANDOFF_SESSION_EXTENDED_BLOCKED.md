# Handoff: Extended verification blocked by timeout + float drift (baseline preserved)

## What changed

Nothing committed in this session. Working tree is clean (`git status --short` empty).
The pinned dependencies are installed and match `requirements.txt` exactly
(numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0,
yfinance 1.7.0) on Python 3.12.3. The 2026-10-12 data vintage is cached in `data/`.

## What was actually verified (evidence)

**`SEED=42 bash scripts/check.sh` -> `=== All checks passed ===` (exit 0)**
- 107/107 committed JSON artifacts parse OK (`scripts/check_json_artifacts.py`)
- Convention robustness: PASS (15 strategies + 8 E024 decompositions + E042 gates; E042 PARTIAL 4/5 as recorded)
- Template validation: OK
- All 27 experiment scripts import OK (`scripts/check_experiment_imports.py`)

**`SEED=42 python3 run_all_verification.py --extended` -> did NOT complete**
- Terminated by shell timeout after >40 min, mid `[5b/7/18] run_e019.py`.
- Before termination, killed mid-run so the `try/finally` golden-restore block did NOT run;
  10 experiment JSONs were overwritten by fresh output. I restored them with
  `git restore experiments/`; tree is now clean again. No goldens were permanently modified.

Partial extended results observed before timeout:
- 5a quick block: e012, e023, e024 EXACT; e027/e035 deterministic EXACT; e037 27 float mismatches (~1e-7, known drift); e039 EXACT; e042_lead 22 mismatches (known stale golden, REJECTED decision unchanged, exit=1 as expected).
- 5b extended block: e011 PASS (match, numeric_tol=1e-4); e013 PASS (match); **e015 FAIL** (150 numeric diffs, e.g. is_ann_return 0.13810->0.13790 ~0.14%); **e016 FAIL** (56 diffs incl. STRING diff `/universe/end: '2026-10-12' -> '2026-10-09'` and `/universe/n_days: 2327 -> 2326`); **e017 FAIL** (55 numeric diffs); **e018 FAIL** (55 numeric diffs). e019-e041 unknown (timed out).

## What remains unresolved

- The extended verification suite does **not** report `ALL CHECKS PASSED` under the
  current environment: multiple committed goldens (e015, e016, e017, e018 at minimum)
  exceed the `numeric_tol=1e-4` bound, and e016 has a structural/string difference
  in the data end date. The suite also takes >40 min (exceeds practical blocking bound).
- Root cause of the float drift is not yet confirmed: likely environment-induced
  (dependency versions vs the environment used to generate the committed goldens,
  and/or data cache end-date resolution for e016), NOT a code regression — the E031
  JSON bracket fix cannot affect computation, and the tree is otherwise unchanged.

## Which approaches have already failed and why

- Re-running `run_all_verification.py --extended` as a single blocking call: FAILS
  (timeout >40 min, incomplete). Repeating it unchanged would hit the same timeout
  and the same float-drift failures — not a materially different approach.
- Weakening `numeric_tol` or skipping drivers: prohibited by task constraints
  ("do not weaken comparison tolerances or skip drivers to make it pass").
- Modifying committed goldens to absorb drift: prohibited by constraint
  ("Do NOT modify committed goldens").

## One precise next task

Run `SEED=42 python3 run_all_verification.py --extended` **to completion in a
long-running/background context** (it needs >40 min) and record verbatim:
  (a) which drivers FAIL and their drift magnitudes,
  (b) whether e019-e041 pass or fail.
Do NOT modify goldens, tolerances, gate logic, sensitivity grids, pre-registered
outcomes, or validated constructions (`src/*`).

Based on that evidence, determine whether the drift is environment-induced
(dependency versions vs golden-generation environment, and e016's end-date
resolution 2026-10-12 vs 2026-10-09) and document it as a reproducibility caveat,
or escalate to a maintainer for a tolerance / golden-regeneration decision.
Do not blindly repeat the 40-minute blocking run without a plan to capture the
full result.

### Constraints
- Honor `SEED=42` and the cached 2026-10-12 parquet vintage.
- Do not change `run_all_verification.py` comparison logic or tolerances.
- Preserve the snapshot/restore mechanism; if the run is killed again, restore
  `experiments/` with `git restore experiments/` before anything else.
