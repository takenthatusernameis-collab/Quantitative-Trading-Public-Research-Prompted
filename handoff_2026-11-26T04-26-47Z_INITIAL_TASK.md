# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-26T04-26-47Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State

- **Phase:** Research complete (E001–E043)
- **Validated strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden artifacts:** `experiments/*.json` (canonical baseline, SHA-256 pinned in `ledger/golden_baseline.json`)
- **Data vintage:** 2026-10-12 (pinned in `data/vintages.json`); 2026-10-11 (committed for E026/E028/E029/E030/E034/E036/E037)
- **E029 fundamentals:** Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` (offline-reproducible when `SEED` is set)
- **Working tree:** Clean except one tracked build-noise modification: `src/__pycache__/cache_keys.cpython-312.pyc` (safe to ignore / `git checkout --` to restore)
- **HEAD:** `0d15998d` on branch `main`

## Verification Commands (SEED=42)

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full

# Recover the golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Critical Integrity Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. If `HEAD` already carries a captured run, restore the pinned artifact with `git checkout <commit> -- experiments/<file>` where `<commit>` matches `ledger/golden_baseline.json`.
2. **Golden baseline is pinned** in `ledger/golden_baseline.json` (SHA-256). Do not re-pin as a side effect of verification; re-pin only for a deliberate, ledger-recorded code change.
3. **Data coverage is enforced** — `scripts/check_data_coverage.py` requires every cache file to exist, be git-tracked, and match `ledger/data_baseline.json`. The suite runs offline (`QUANT_RESEARCH_OFFLINE=1`); a missing cache entry fails hard.
4. **Optimizer determinism** — SLSQP status 8 is valid at a constrained optimum; gating on it caused environment-dependent E042 (fixed by E050 exact active-set enumeration). Do not re-pin E041/E042 to silence tolerance violations.
5. **CI gate cannot be created by agents** — template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via the GitHub UI.
6. **Dependencies NOT provisioned this session** — run `pip install -r requirements.txt` first (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional).

## Initial Task

Default: await explicit user instructions. If acting autonomously:

1. Verify working-tree cleanliness against HEAD (`git status`); the only expected diff is the `src/__pycache__/*.pyc` build-noise file.
2. Run `SEED=42 bash scripts/check.sh` (fast convention-robustness check: goldens clean, golden baseline, data coverage, optimizer determinism).
3. If clean, reproduce with `SEED=42 python3 run_all_verification.py --extended` and report any drift; do NOT re-pin goldens.
4. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` before committing anything.

## Last Verification Status

Not run in this session. Run `SEED=42 python3 run_all_verification.py --extended` to verify current state. The extended suite re-executes the committed drivers and compares against goldens with `numeric_tol=1e-4`.

## Durable Handoff Pointers

- `handoff_CURRENT.md` -> this file (latest handoff)
- `handoff_LATEST.md` -> this file
- `handoff_NEXT.md` -> this file (next session initial task)
- Prior handoffs: `handoff_<timestamp>Z_INITIAL_TASK.md` (immutable history)