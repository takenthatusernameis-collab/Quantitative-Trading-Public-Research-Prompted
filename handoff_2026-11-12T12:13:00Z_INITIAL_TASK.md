# Agentic Handoff — Initial Task

**Created:** 2026-11-12T12:14:47Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical research artifacts live in `experiments/*.json` (committed goldens).
- Baseline integrity rules enforced by `scripts/check.sh` (`check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`) — see `AGENTS.md` "Baseline Integrity".
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). cvxpy optional; optimizer falls back to scipy.
- No pending verification run; `.verify_snapshot/` is clean (no `ACTIVE.json`).

## Initial task for next session

Pick up where research left off OR run the local convention check first to establish a clean baseline:

```bash
SEED=42 bash scripts/check.sh
#   or
make check
```

Then, if a new experiment or driver is requested:
1. Pre-register with a `pre_registered` JSON block (gates, falsification expectations, sensitivity grid).
2. Run the driver; do NOT commit verification output under `experiments/`.
3. Restore goldens after any run: `SEED=42 python3 run_all_verification.py --restore-only`.
4. Any new data input must be committed + re-pinned via `python3 scripts/check_data_coverage.py --update`.
5. Never re-pin a golden as a side effect of a verification run; re-pinning requires `--update` on `check_golden_baseline.py`.

## Do NOT

- Do not create `.github/workflows/verification-gate.yml` (controller restores/cleans it; token lacks push permission).
- Do not commit driver output to `experiments/`.
- Do not commit secrets/keys.

## Reference commands

- Quick verify (~8 min): `SEED=42 python3 run_all_verification.py` / `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended`
- Full: `SEED=42 python3 run_all_verification.py --full`
- Recover interrupted run: `SEED=42 python3 run_all_verification.py --restore-only`
