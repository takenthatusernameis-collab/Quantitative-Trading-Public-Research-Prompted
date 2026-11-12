# Agentic Handoff — Initial Task

**Created:** 2026-11-12T13:04:50Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical research artifacts live in `experiments/*.json` (committed goldens).
- Baseline integrity rules enforced by `scripts/check.sh` (`check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`) — see `AGENTS.md` "Baseline Integrity".
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). cvxpy optional; optimizer falls back to scipy.
- No pending verification run; `.verify_snapshot/` is clean (no `ACTIVE.json`).
- `git status` shows only a stray `__pycache__/cache_keys.cpython-312.pyc` modification (untracked/build artifact); working tree otherwise clean at `53191374 chore(kilo): checkpoint agent session`.

## Initial task for next session

1. Establish a clean baseline with the convention-robustness check (fast, offline, seconds):

   ```bash
   SEED=42 bash scripts/check.sh
   #   or
   make check
   ```

2. If a new experiment/driver is requested:
   - Pre-register with a `pre_registered` JSON block (gates, falsification expectations, sensitivity grid) per the ledger entry format.
   - Run the driver; do NOT commit verification output under `experiments/`.
   - Restore goldens after any run: `SEED=42 python3 run_all_verification.py --restore-only`.
   - Any new data input must be committed + re-pinned via `python3 scripts/check_data_coverage.py --update`.
   - Never re-pin a golden as a side effect of a verification run; re-pinning requires `--update` on `check_golden_baseline.py`.

3. Optional deeper verification:
   - Quick (~8 min): `SEED=42 python3 run_all_verification.py` / `make verify-quick`
   - Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended`
   - Full (~15 min): `SEED=42 python3 run_all_verification.py --full`
   - Recover interrupted run: `SEED=42 python3 run_all_verification.py --restore-only`

## Do NOT

- Do not create `.github/workflows/verification-gate.yml` (controller restores/cleans it; token lacks push permission). Template at `.github/workflow-templates/verification-gate.yml`.
- Do not commit driver output to `experiments/`.
- Do not commit secrets/keys.

## Reference

- `AGENTS.md` — project commands, conventions, baseline integrity, reproducibility.
- `ledger/RESEARCH_LEDGER.md` — all experiment entries E001–E043 with statuses and decisions.
