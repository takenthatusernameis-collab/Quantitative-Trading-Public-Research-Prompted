# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-30 00-44-41ZZ (message time)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ a9813ec (2026-10-30 00:43:34, "chore(kilo): checkpoint agent session")
**Preceding handoff:** HANDOFF_NEXT_SESSION_2026-10-30T00-42-23Z.md

## Current State (verified at handoff time)

- **Working tree:** clean of tracked changes (only gitignored artifacts possible).
- **No live snapshot:** `.verify_snapshot/` absent. No verification run in progress.
- **Experiment artifacts:** 107 committed JSONs under `experiments/` (E001–E043). Research phase complete.
- **Research phase:** complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `tests/test_portfolio_opt.py`, `verify_convention_robustness.py` all in place.

## INITIAL TASK (START HERE - MANDATORY)

**Task:** Establish and confirm a clean baseline before doing any new work.

Execute these steps in order:

### Step 1: Verify all guards pass
```bash
SEED=42 bash scripts/check.sh
```
Expected: All checks green (goldens clean vs HEAD, golden baseline SHA-256 match, data coverage, portfolio-opt tests, py_compile, convention robustness, template validation).

### Step 2: Confirm working tree state
```bash
git status --short && git diff --name-only
```
Expected: Only untracked/build-artifact `__pycache__/*.pyc` files (gitignored). No tracked source/data modifications.

### Step 3: Report baseline status
After steps 1-2 complete successfully, report:
- `check.sh` exit code and summary
- `git status --short` output
- Any warnings or failures (if any) with proposed fixes

**If check.sh fails:** Diagnose and fix issues before proceeding. Do NOT commit verification outputs or re-pin baselines to silence drift. See constraints below.

## Known Pre-Existing Drift (reporting-only, do NOT re-pin)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone. Open item in ledger.
- **E030**: numeric diffs on near-zero quantities (ledger E048). Input committed, golden deliberately re-pinned.
- **E029**: offline-reproducible (fundamentals pinned in `data/fundamentals/`), golden deliberately re-pinned. Reproduces with 0 differences.

## Constraints (STRICT - DO NOT VIOLATE)

- Always use `SEED=42`.
- Never leave `run_all_verification.py` half-finished. Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. Suite self-recovers at startup.
- **Do NOT re-pin goldens or `ledger/golden_baseline.json` / `ledger/data_baseline.json` to silence drift.** Committed baselines are authoritative.
- Do **not** commit verification outputs (`.verify_reports/`, driver re-runs).
- Honor pinned cache vintages (`data/vintages.json`, `data/fundamentals_vintages.json`). Verification uses `QUANT_RESEARCH_OFFLINE=1`; missing cache fails hard.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`).

## Quick Commands

```bash
SEED=42 bash scripts/check.sh                    # fast offline guard suite (START HERE)
SEED=42 python3 run_all_verification.py        # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # (~21 min)
SEED=42 python3 run_all_verification.py --full    # (~15 min)
SEED=42 python3 run_all_verification.py --restore-only # recover if interrupted
```
