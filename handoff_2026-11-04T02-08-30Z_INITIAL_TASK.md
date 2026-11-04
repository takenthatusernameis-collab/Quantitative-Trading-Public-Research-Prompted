# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T02:08:30Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 98b2418051232c4646aea973874ba50ef2ecfb76 (matches `origin/main`)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean (0 modified tracked files; only `__pycache__/*.pyc` untracked)

## Session Summary (what happened this session)

- Inspected repo state: research phase complete (E001–E043); surviving strategies in `ledger/RESEARCH_LEDGER.md`.
- Found a **stale, interrupted-verification snapshot** at `.verify_snapshot/ACTIVE.json` (owner pid 41335, started 2026-11-04T01:07). PID 41335 is no longer running.
- Verified snapshot integrity before touching anything:
  - `diff -rq .verify_snapshot/experiments experiments` → 0 JSON differences (only `.py` driver files exist in the live tree, not in the snapshot).
  - `git diff --stat HEAD -- experiments` → empty; committed goldens untouched.
- **Recovered the snapshot** (clears the stale ACTIVE marker, restores goldens):
  ```bash
  SEED=42 python3 run_all_verification.py --restore-only
  ```
  Output: `RESTORE COMPLETE: golden artifacts restored from the pending snapshot.`
- Confirmed cleanup: `.verify_snapshot/ACTIVE.json` gone; `git status` clean.
- **Ran `SEED=42 bash scripts/check.sh` → ALL CHECKS PASSED** (experiment script imports + calls; golden-baseline integrity; data coverage). Baseline is healthy and ready for any verification run.

## Initial Task

Research phase complete (E001–E043); surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. The baseline is now clean and recoverable.

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Verification Commands (if explicitly asked to reproduce)

```bash
SEED=42 python3 run_all_verification.py            # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended # (~21 min, +18 committed drivers)
SEED=42 python3 run_all_verification.py --full     # (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after an interrupted run
SEED=42 python3 verify_convention_robustness.py     # convention robustness only (reads JSONs, no writes)
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents (see AGENTS.md). Use local `make check/verify/*`.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs. This file is the authoritative initial-task message for the next session.
Durable copies written to: `handoff/`, `.kilo/handoff/`, and root symlink targets updated.

Handoff written by agent at 2026-11-04T02:08:30Z.