# Session Handoff: extended verification ran; 3 drift-class failures; tree clean

## What changed (this session)
- Nothing in the repository. No code, no golden, no ledger, no doc changes.
- Only ran `SEED=42 python3 run_all_verification.py --extended` (~21 min) via background process; it completed, restored all experiment JSONs from `.verify_snapshot/`, and left the working tree clean (confirmed `git status --short` empty; no `.verify_snapshot/` dir remains).

## What was actually verified (evidence)
Full `run_all_verification.py --extended` completed and printed `VERIFICATION SUMMARY` / `OVERALL: FAILURES DETECTED`:
- [PASS] check_json_artifacts, test_json_guard, check_goldens_clean, verify_convention_robustness, batch_run, validate
- [PASS] run_e012, e023, e024, e027, e035, e037, e039 (5a block, all match)
- [FAIL] run_e042_lead.py (exit 1 — pre-registered REJECTED decision; detailed comparison showed 5 small `placebo_constrained` numeric mismatches beyond numeric_tol=1e-4, e.g. z_score 1.9568→1.9578, mean_sharpe 0.5721→0.5720)
- [PASS] run_e011, e013, e015, e016, e017, e018, e019, e020, e021, e022, e025, e026, e028 (5b block)
- [FAIL] run_e029.py (structural match, numeric drift beyond 1e-4)
- [PASS] run_e030.py
- [FAIL] run_e034.py (structural match, numeric drift beyond 1e-4)
- [PASS] run_e036, e041, run_e042 (quick n_sim=2)
- OVERALL: FAILURES DETECTED

## What remains unresolved
- 3 drift-class failures (e042_lead, e029, e034) cannot be "fixed" without violating repo rules: do NOT weaken tolerances, do NOT skip drivers, do NOT modify committed goldens, do NOT regenerate goldens. All are "structural match" (no added/missing keys, no list-length changes) — pure bounded floating-point drift in stochastic/placebo fields.
- **New, important finding**: the failing set is NOT stable across runs. Prior documented runs failed e022/e030/e041 or e029/e030/e041; this run failed e029/e034/e042_lead (e030 and e041 now PASS). This indicates OpenBLAS/numpy floating-point nondeterminism across runs (~1e-4 to 1e-3 drift) sometimes crosses the `numeric_tol=1e-4` threshold. The `--extended` suite is therefore not a stable "all pass" gate on this machine.
- Per AGENTS.md this drift class is already acknowledged ("A few drivers exhibit small floating-point drift between runs... comparison accepts bounded numeric drift while still failing on any structural/string difference").

## Which approaches have already failed and why
- None attempted in this session (no changes made). Prior sessions rejected: regenerating goldens, weakening tolerances, skipping drivers (all forbidden by goalpost/baseline discipline).

## One precise next task
Decide the disposition of the drift-class failures. Two options:
1. Accept as documented floating-point drift (consistent with AGENTS.md; record verbatim in `ledger/RESEARCH_LEDGER.md` alongside existing E022/E030/E041 drift caveats, noting the failure-set instability evidence above) and close the item — no code change.
2. Investigate BLAS/numpy determinism (e.g. pin `OMP_NUM_THREADS=1` / `OPENBLAS_NUM_THREADS=1`) to see if the comparisons become stable — only if a maintainer considers the flaky gate a real problem; this is an infrastructure change, not a research change, and is out of scope unless explicitly requested.

Do NOT re-run `--extended` expecting a different result without one of the above decisions or a material change (e.g. thread pinning), since the result is nondeterministic.

Constraints: `SEED=42`, cached 2026-10-12 parquet vintage, no committed-golden modification, no tolerance/driver/skip changes.
