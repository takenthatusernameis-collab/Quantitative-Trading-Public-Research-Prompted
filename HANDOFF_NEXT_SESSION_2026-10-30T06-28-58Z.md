# HANDOFF — 2026-10-30T06:28:58Z

## Clear Initial Task for Next Session

**Goal:** Recover stale verification state, then verify baseline integrity and establish a clean verification state before any new work.

## Critical: Stale Snapshot Present

A live verification snapshot exists but its owner process is dead:

- `.verify_snapshot/ACTIVE.json` holds pid **33924**, started 1793341567.3073428.
- `ps -p 33924` → process not found (dead since before this handoff).
- `scripts/check_goldens_clean.py` will FAIL while a stale snapshot is pending.

**Step 0 — Recover first (do NOT start a new verification run until this is done):**
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or: git checkout -- experiments/
```
Then confirm `.verify_snapshot/ACTIVE.json` is gone and `git status --short` shows no experiment changes (only __pycache__ noise is acceptable).

## Step 1 — Baseline Integrity Guards
```bash
SEED=42 bash scripts/check.sh
```
Runs: py_compile, `check_goldens_clean.py` (tree vs HEAD), `check_golden_baseline.py` (vs `ledger/golden_baseline.json`), `check_data_coverage.py`, convention robustness tests. All must pass.

## Step 2 — Quick Verification (if Step 1 passes)
```bash
SEED=42 python3 run_all_verification.py
```
~8 min. Restores goldens automatically. Confirms 8 quick drivers + batch/validate + E042 n_sim=2 reproduce correctly.

## Step 3 — Report Status
Summarize: snapshot recovery result, any golden mismatches and resolution, data coverage result, quick verification pass/fail, anomalies vs extended drift expectations.

## Known Open Items (do not re-pin to silence)
- E041: 133 numeric diffs remain due to ill-conditioned QP sensitivity; 3 structural diffs eliminated. Reported in extended summary only.
- E042/E041 grid can drift by 1-ulp; do not re-pin artifacts to mask this.

## Constraints
- Never commit verification output. Restore before committing.
- Never re-pin goldens/data as a side effect of verification; only via explicit `--update`.
- Always use `SEED=42`.
- Verification uses `QUANT_RESEARCH_OFFLINE=1`; all caches must be pinned.
- E041/E042 numeric drift is expected; focus on structural differences.

## Key References
- `AGENTS.md` — commands, conventions, baseline integrity rules
- `ledger/RESEARCH_LEDGER.md` — experiment history and decisions
- `ledger/golden_baseline.json` / `ledger/data_baseline.json` — pinned fingerprints
- `run_all_verification.py` — verification orchestrator

**Start at Step 0. Do not begin new experiments until Steps 0–2 pass cleanly.**
