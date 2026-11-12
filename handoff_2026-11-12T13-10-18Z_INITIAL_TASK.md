# Agentic Handoff — Initial Task

**Created:** 2026-11-12T13:10:18Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** `61a6e14ced4ba6b886bae16510ef02d99131c28f` (2026-11-12 13:08:19 +0000, `chore(kilo): checkpoint agent session`, `main` = `origin/main`, in sync)

## Verified state (checked 2026-11-12T13:10:18Z)

- Research phase complete (E001–E043). Surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`.
- Last research entry is E051 (2026-11-02); E052–E169 are durable-handoff refreshes only. No actionable OPEN/PENDING/BLOCKED/TODO markers.
- `python3 scripts/check_golden_baseline.py` -> ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT.
- `python3 scripts/check_data_coverage.py` -> ALL 35 PINNED DATA INPUTS PRESENT, TRACKED AND UNCHANGED.
- `git diff HEAD -- experiments/ data/` -> empty. `git ls-files experiments/` -> 138 tracked entries (107 goldens + 31 drivers).
- No interrupted verification: `.verify_snapshot/` absent. An `ACTIVE.json` from an unrelated self-test names pid 999999 / pid 36305, both not running.
- `git status --short` shows only tracked `__pycache__/*.pyc` byte/timestamp drift (src/, scripts/, tests/). This is build noise, not canonical. Do not commit it.

## Environment caveat (important)

`SEED=42 bash scripts/check.sh` exits 1 in this sandbox for environmental reasons, not code defects:
- `/usr/bin/python3` (3.12.3) has **none** of `requirements.txt` installed (`numpy`, `pandas`, `scipy`, `pyarrow`, `statsmodels`, `yfinance` all missing). `tests.test_data_coverage` and `tests.test_portfolio_opt` fail with `ModuleNotFoundError`.
- Other check.sh steps pass: `check_json_artifacts.py`, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `test_json_guard`, `test_goldens_guard`, `test_golden_baseline`, `test_drift_report`, `verify_convention_robustness.py`, `validate_template.py`, `check_experiment_imports.py`.
- FAIL lines printed by `test_json_guard` are its own negative fixtures in a temp git repo, not real artifacts.
- `experiments/e042_quick.json` is pre-existing untracked and unrelated.

To get a green suite: `pip install -r requirements.txt` first.

## Initial task for next session

1. Establish a clean baseline (after installing deps, or at minimum the offline guards):
   ```bash
   SEED=42 bash scripts/check.sh
   # or: make check
   ```

2. If a new experiment/driver is requested:
   - Pre-register before execution: `pre_registered` JSON block (gates, falsification expectations, sensitivity grid) per the ledger entry format.
   - Run the driver; never commit driver/verification output under `experiments/`.
   - Restore goldens after any run: `SEED=42 python3 run_all_verification.py --restore-only`.
   - New data input: commit it, then re-pin with `python3 scripts/check_data_coverage.py --update`.
   - Never re-pin goldens as a side effect of verification; re-pin only deliberately via `python3 scripts/check_golden_baseline.py --update`.

3. Verification levels (if requested):
   - Quick (~8 min): `SEED=42 python3 run_all_verification.py` / `make verify-quick`
   - Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended`
   - Full (~15 min): `SEED=42 python3 run_all_verification.py --full`
   - Recover an interrupted run: `SEED=42 python3 run_all_verification.py --restore-only`

## Do NOT

- Do not create `.github/workflows/verification-gate.yml` (controller restores/cleans it; token lacks push permission). Use template `.github/workflow-templates/verification-gate.yml`.
- Do not commit driver/verification output to `experiments/`, secrets, or `src/__pycache__`/`scripts/__pycache__`/`tests/__pycache__`.
- Do not move gateposts post-hoc or re-pin baselines to silence drift.

## References

- `AGENTS.md` — commands, reproducibility, baseline integrity rules.
- `ledger/RESEARCH_LEDGER.md` — E001–E169 records/dispositions.
- `ledger/PRIORITIZATION.md` — ranking criteria and procedure.