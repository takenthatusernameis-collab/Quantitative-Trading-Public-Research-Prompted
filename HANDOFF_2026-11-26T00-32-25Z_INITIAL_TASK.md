# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-26T00:32:25Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 1404e2e9b19dbf3d3610d354cbcb6c62aeb4a169 (2026-11-26 00:32:16 +0000)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean for canonical artifacts (`experiments/`, `data/`, `ledger/`). No live verification run; `.verify_snapshot/` and `.verify_reports/` absent.

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*
- Wrote durable initial-task handoff `HANDOFF_2026-11-26T00-32-25Z_INITIAL_TASK.md` at repo root, superseding prior INITIAL_TASK handoffs (most recent prior: `HANDOFF_2026-11-24T21-08-52Z_INITIAL_TASK.md`).
- Verified repository state against live HEAD before writing: HEAD == `1404e2e9b19dbf3d3610d354cbcb6c62aeb4a169` (2026-11-26 00:32:16 +0000); `git status --short experiments/ data/ ledger/` empty; no `.verify_snapshot/` (no interrupted run to recover).
- Did **not** run verification, modify experiments, change baselines, or take any research action. No explicit user direction beyond the handoff request. Left uncommitted pending explicit direction.

## CLEAR INITIAL TASK

**Await explicit user instructions before any research action.**

The next agentic work session must:

1. Confirm canonical state: `git log -1 --format="%H"`, `git status --short experiments/ data/ ledger/`, confirm HEAD == origin/main, confirm no `.verify_snapshot/` exists.
2. Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items (research phase closed, E001–E043).
3. Optionally run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green — only if the user directs it.
4. If the session itself hands off, create its own timestamped durable handoff following the established pattern (`HANDOFF_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root).

Do **not** re-run verification, modify experiments, or change baselines without explicit direction. Do **not** invent new tasks, create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

## First Steps (verify state)

- `git log -1 --format="%H"` and `git status --short experiments/ data/` — confirm HEAD == origin/main and canonical artifacts unmodified.
- Confirm no `.verify_snapshot/` directory exists (no interrupted run to recover).
- Read `ledger/RESEARCH_LEDGER.md` for the surviving validated strategies and open items.
- Quick check before any change: `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green.

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs (most recent prior: `HANDOFF_2026-11-24T21-08-52Z_INITIAL_TASK.md`). This file is the authoritative initial-task message for the next session.

Handoff written by agent at 2026-11-26T00:32:25Z.
