# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T06-57-53Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 7610ca56cecf9d3c76e9a9f626389a409b149a3c (== origin/main)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean (only __pycache__ artifacts). No live verification run; `.verify_snapshot/` absent. No source/test/ledger change.

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !*
- Verified repository state against live HEAD before writing: HEAD == origin/main (`7610ca5`), tracked tree clean aside from __pycache__, no uncommitted source changes, `.verify_snapshot/` absent.
- Prior active handoff was `handoff/handoff_2026-11-04T06-06-03Z_INITIAL_TASK.md` (and root/.kilo/handoff variants). This new handoff supersedes them and is the authoritative initial-task message for the next session.
- Did **not** run verification, modify experiments, change baselines, or take any research action. No explicit user direction beyond the handoff request.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !*

The next agentic work session must create its own timestamped durable handoff following the established pattern (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` under `handoff/`, mirrored at root and `.kilo/handoff/`) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. The baseline is clean and recoverable. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

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
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs (most recent prior: `handoff/handoff_2026-11-04T06-06-03Z_INITIAL_TASK.md`, root `handoff_2026-11-04T06-06-03Z_INITIAL_TASK.md`). This file is the authoritative initial-task message for the next session.
Durable copies written to: `handoff/`, root, `.kilo/handoff/`.

Handoff written by agent at 2026-11-04T06:57:53Z.
