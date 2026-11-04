# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T14-53-58Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 830709bafb4c4adb387a5eb49c8e220a01ba0e00 (2026-11-04 14:52:46 +0000 chore(kilo): checkpoint agent session)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean for `experiments/` and `data/` (no live verification run; `.verify_snapshot/` absent). Only `__pycache__/*.pyc` show mtime/mode drift vs HEAD (if any) — not a baseline problem.

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*
- Did **not** run verification, modify experiments, change baselines, or take any research action. No explicit user direction beyond the handoff request.
- Supersedes previous INITIAL_TASK handoff `handoff_2026-11-04T13-57-54Z_INITIAL_TASK.md`.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must create its own timestamped durable handoff following the established pattern (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root, repointing `handoff_next_session.md`) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. The baseline is clean and recoverable. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items.

## First Steps (verify state)

- `git log -1 --format="%H"` and `git status --short experiments/ data/` — confirm HEAD == origin/main and canonical artifacts unmodified.
- Confirm no `.verify_snapshot/` directory exists (no interrupted run to recover).
- Read `ledger/RESEARCH_LEDGER.md` for the surviving validated strategies and open items.
- Quick check: `SEED=42 bash scripts/check.sh` (or `make check`) before any change, to confirm goldens + data coverage + JSON guards are green.

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoff `handoff_2026-11-04T13-57-54Z_INITIAL_TASK.md`. This file is the authoritative initial-task message for the next session.

Handoff written by agent at 2026-11-04T14-53-58Z.
