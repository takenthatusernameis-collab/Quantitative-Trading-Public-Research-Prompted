# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T07-06-06Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 74dcf2500a019d5fd1e85d85231fb1e4f79fc0b2
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** 0 modified files in canonical dirs 0

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !*
- Verified repository state: HEAD matches origin/main, no live verification run in progress.
- Supersedes previous INITIAL_TASK handoffs. This file is the authoritative initial-task message for the next session.
- Did **not** run verification, modify experiments, change baselines, or take any research action.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must create its own timestamped durable handoff following the established pattern (`handoff/YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` under `handoff/`, mirrored at root and `.kilo/handoff/`, repointing all root + `.kilo/handoff/` + `handoff/` symlinks) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items.

## First Steps (verify state)

- `git log -1 --format="%H"` and `git status --short experiments/ data/` — confirm HEAD clean
- Confirm no `.verify_snapshot/` directory exists
- Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items
- Quick check: `SEED=42 bash scripts/check.sh` (or `make check`) before any change

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs. This file is the authoritative initial-task message for the next session.
Durable copies written to: `handoff/`, root, `.kilo/handoff/` (symlinks updated as applicable).

Handoff written by agent at 2026-11-04T07-06-06Z.
