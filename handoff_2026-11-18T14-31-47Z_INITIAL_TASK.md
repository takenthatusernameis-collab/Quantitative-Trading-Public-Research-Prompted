# Agentic Work Session Handoff — INITIAL TASK

**Timestamp:** 2026-11-18T14:31:47Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Repo HEAD at write time:** `74f54429a6c69ea368e4310bb7323ccbdc51f720` (`origin/main` identical, 0 ahead / 0 behind)

## START HERE — Initial Task for the Next Session

1. **Confirm the environment.** Run the fast offline integrity gate:
   `SEED=42 bash scripts/check.sh` (or `make check`). This validates the JSON
   templates, golden cleanliness, the pinned golden baseline, cache coverage,
   and `tests/test_portfolio_opt.py`.
2. **Install deps if the gate cannot start.** On a bare runner the system
   interpreter is `/usr/bin/python3` 3.12.3 and core packages are absent
   (`import pandas` → `ModuleNotFoundError`). Fix with
   `python3 -m pip install -r requirements.txt` (numpy, pandas, scipy,
   pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional).
3. **Only if asked to re-verify research**, pick a level and let it finish:
   - `SEED=42 python3 run_all_verification.py` (`make verify-quick`, ~8 min)
   - `SEED=42 python3 run_all_verification.py --extended` (~21 min)
   - `SEED=42 python3 run_all_verification.py --full` (~15 min)
4. **Do not start new research or move goalposts.** Research phase is complete
   (E001–E051 in `ledger/RESEARCH_LEDGER.md`). This handoff refresh adds no
   experiment; the deliverable is continuity only.
5. **If the user only asks for another handoff refresh**, repeat the existing
   convention: write `handoff_<UTC ISO>_INITIAL_TASK.md` at repo root, mirror
   byte-identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`,
   `.kilo/handoff/`, run
   `python3 scripts/repoint_handoff.py handoff_<UTC ISO>_INITIAL_TASK.md`,
   and append the next `E###` ledger entry under `## Handoff Refreshes`.

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US
equities, futures, and macro data. Every experiment is pre-registered with
falsification expectations and promotion gates. Surviving validated strategies
are documented in `ledger/RESEARCH_LEDGER.md`; prioritization history is in
`ledger/PRIORITIZATION.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh          # or: make check

# Quick full verification (~8 min; 8 drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py            # or: make verify-quick

# Extended verification (~21 min; quick + 18 more drivers, structural match)
SEED=42 python3 run_all_verification.py --extended # or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full     # or: make verify-full

# Recover goldens after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Current State (verified 2026-11-18T14:31Z)

- `git status --short` → clean (apart from 15 tracked `__pycache__/*.pyc`
  bytecode churn, which is pre-existing and not committed).
- `git diff --name-only HEAD -- experiments/` → empty: all committed golden
  artifacts match HEAD.
- No `.verify_snapshot/ACTIVE.json` and no `.verify_reports/`: no verification
  run is in progress or half-finished.
- No active research task; repository closed for research (E001–E051).

## Key Integrity Notes

- **Golden files**: `experiments/*.json` are the canonical committed artifacts.
  The verification suite backs them up (`.verify_snapshot/`, gitignored) and
  restores them afterwards. The committed golden is the authoritative record,
  not the latest re-run.
- **Baseline guards**: `scripts/check_goldens_clean.py` (working tree vs HEAD)
  and `scripts/check_golden_baseline.py` (SHA-256 pinned in
  `ledger/golden_baseline.json`) are first-class steps of `scripts/check.sh`.
- **Data cache**: pinned vintages in `data/vintages.json` and
  `data/fundamentals_vintages.json`; coverage is enforced by
  `scripts/check_data_coverage.py` against `ledger/data_baseline.json`. An
  unpinned input becomes a non-reproducible network download.
- **Reproducibility**: always `SEED=42`. Close-to-close is the v1.2.3 primary
  convention; overnight decomposition is reported alongside.
- **Known drift (documented, do NOT "fix" by re-pinning)**: E041/E042 grid
  artifacts still drift by ~29–133 numeric differences because the tangency QP
  is ill-conditioned (1-ulp sensitivity). Decisions and gate flags are
  unchanged. Never re-pin a golden to silence drift as a side effect of
  verification; re-pinning requires `--update` and must be an explicit diff.

## Important Guards

- Never leave a verification run half-finished: it overwrites goldens mid-run.
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`, or
  `git checkout -- experiments/` (and if HEAD itself captured a run, restore
  from the last commit matching `ledger/golden_baseline.json`).
- Do not commit verification output, re-pinned baselines, or `__pycache__`.
- Do not commit changes unless explicitly asked.

## Provenance

This refresh supersedes `handoff_2026-11-18T14-30-25Z_INITIAL_TASK.md` (and the
unrecorded `handoff_2026-11-18T14-28-*` files), which were written without an
intervening ledger entry. Provenance is recorded as ledger entry E497 against
live HEAD `74f54429`.
