# Session Handoff 2026-10-18 (e)

## What changed
- No source code or committed artifact was modified. Working tree is clean (`git status --short` empty).
- Ran the fast offline suite: `SEED=42 bash scripts/check.sh` -> `=== All checks passed ===` (exit 0). Covers: JSON artifact guard (107/107 committed artifacts parse), 19 unit tests in tests/test_json_guard.py, convention robustness (15 strategies + 8 E024 decompositions + E042 gates), template validation, all 26 experiment script imports.
- Confirmed scientific dependencies ARE installed (numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow, statsmodels, yfinance) — the HANDOFF_NEXT.md/NEXT_HANDOFF.md claim that they are not installed is stale for this environment.
- Attempted `SEED=42 python3 run_all_verification.py --extended` (~21 min). It ran ~25 min then was killed by the shell timeout at [5b/7/18] run_e019.py. Because the process was killed, the script's backup/restore `finally` block did not run; I manually restored the 9 overwritten experiment JSONs via `git checkout -- experiments/` (tree clean).

## What was actually verified (evidence)
- check.sh fast path: ALL CHECKS PASSED (exit 0).
- --extended, 5a block (8 drivers E012,E023,E024,E027,E035,E037,E039,E042-lead): all matched committed goldens (excl timestamp, numeric_tol=1e-4).
- --extended, 5b block: E011, E013, E015 matched goldens exactly.
- --extended, 5b block: E016/E017/E018 show drift beyond the 1e-4 relative tolerance vs committed goldens.
- Ground-truthed E016 determinism: `SEED=42 python3 experiments/run_e016.py` run twice -> identical results both times (tsm_deseamed OOS Sharpe=0.717, placebo z=3.06). Committed golden records placebo_z=2.82. So the E016 golden is STALE: a fresh SEED=42 run on the pinned 2026-10-12 vintage deterministically produces 3.06, not 2.82. This is pre-existing, NOT a regression from this session (zero source changes). E017/E018 exhibit similar small beyond-tolerance drifts.

## What remains unresolved
- `--extended` did NOT complete (killed at E019 / [5b/7/18]); E019–E041, batch_run, validate, and E042 quick were never re-run in this session.
- "ALL CHECKS PASSED" for `--extended` cannot be confirmed: E016's committed golden is stale (deterministic fresh value 3.06 vs golden 2.82), so E016 will fail the comparison regardless of re-runs. E017/E018 also drift beyond tolerance.
- Per constraints, I did NOT modify committed goldens or validated constructions (src/*).

## Which approaches failed and why
- `--extended` shell run timed out at 25 min (1500000 ms) before completing; the restore `finally` did not execute (manually reverted).
- Attempting to "make --extended pass" by regenerating goldens is excluded by the constraint "Do NOT modify committed goldens."
- The earlier non-SEED standalone E016 run (placebo z=2.92) was a data-range artifact (end=today 2026-10-18 because SEED was unset), not non-determinism; with SEED=42, E016 is deterministic.

## One precise next task
**Resolve the pre-existing E016/E017/E018 golden staleness so `--extended` reproduces committed goldens within 1e-4, then complete the full `--extended` run.**

Evidence/constraints:
- E016: `SEED=42` fresh run deterministically gives placebo_z=3.06 (verified twice); committed golden says 2.82. Same for E017/E018 (small beyond-tolerance drifts).
- Root cause to determine: whether the committed goldens were generated with different code/data than the current pinned vintage (2026-10-12). Check git history of experiments/e016_futures_tsm_carry.json and the data vintage vs golden creation date.
- Constraints: do not modify goldens or src/* unless a dedicated pre-registered confirmatory run justifies it (per AGENTS.md multiple-testing discipline; goalposts never moved post-hoc). Any golden regeneration must be a deliberate, documented change, not a side effect of verification.
- After resolving, re-run `SEED=42 python3 run_all_verification.py --extended` with a timeout large enough to finish (~45–55 min) and confirm `OVERALL: ALL CHECKS PASSED` and `git status` clean.
- Prerequisite: always invoke with `SEED=42` (data.end_date pinned to 2026-10-12 via data/vintages.json); running without SEED uses today's date and produces non-comparable results.
