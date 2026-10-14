# Handoff: Completed five experiment drivers and convention robustness check

## What changed
- Ran the five experiment drivers (E012, E023, E024--merge, E027, E035) with SEED=42; all completed without error.
- Ran convention robustness check (`verify_convention_robustness.py`) and verified all recorded numbers match.

## What was actually verified
- Each experiment driver executed successfully and produced output files in `experiments/`.
- Convention robustness check passes, confirming that the recorded strategy metrics in the committed goldens are correct under SEED=42 and vintage data.
- No NameError regarding `deterministic_timestamp` (imports fixed in prior session).

## What remains unresolved
- Full verification (`--full`) not executed (~15 min; E042 n_sim=50 + 96-config sensitivity grid). The full E042 golden (`e042_minvar_market_neutral.json`) may have floating-point drift similar to the quick-mode case.
- Batch reproduction (`src/batch_run.py --universe large_liquid`) and validation (`src/validate.py --universe large_liquid`) steps in the verification suite have not been completed due to their long runtime.
- CI gate workflow (`.github/workflows/verification-gate.yml`) still requires maintainer action (GitHub UI) — automated agents cannot push workflows due to controller policy and GITHUB_TOKEN permissions.

## Which approaches have already failed and why
- No approaches have failed in this session; the five experiment drivers and convention robustness check passed.

## One precise next task
Run full verification (`--full`) to confirm the full E042 reproduction (n_sim=50 + sensitivity grid) passes. If the full E042 golden shows drift, regenerate it with `SEED=42 python3 experiments/run_e042.py --n-sim 50` (takes ~10 min). After that, consider running the batch_run and validate steps separately if time permits, as they are slow but necessary for full verification.

### Constraints
- Do not modify committed goldens for E012/E023/E024/E027/E035/E037/E039/E042_lead (verified stable in quick mode).
- Preserve snapshot/restore mechanism in `run_all_verification.py`.
- Do not change gate logic, sensitivity grids, or pre-registered outcomes.
- Honor `SEED=42` and cached parquet (vintage 2026-10-12).