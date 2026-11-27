# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-27T10:51:43Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — ffcf7a489e85dcd6f2d0000116439ade4d07d693 (2026-11-27 10:46:38 +0000)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** `.verify_snapshot/` present with ACTIVE.json (pid 124131) — that process is DEAD. Interrupted verification run pending recovery. Canonical `experiments/`, `data/`, `ledger/` currently match HEAD (git status clean), but a stale snapshot is pending recovery.

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*
- Wrote durable initial-task handoff `HANDOFF_2026-11-27T10-51-43Z_INITIAL_TASK.md` at repo root (this file), superseding prior INITIAL_TASK handoffs (most recent prior: `HANDOFF_2026-11-27T10-46-45Z_INITIAL_TASK.md`).
- Verified repository state against live HEAD before writing: HEAD == `ffcf7a489e85dcd6f2d0000116439ade4d07d693`; `.verify_snapshot/ACTIVE.json` present but owning pid 124131 is dead (interrupted run); `git status --short experiments/ data/ ledger/` clean.

## CLEAR INITIAL TASK

**Recover interrupted verification run first, then await explicit user instructions.**

The next agentic work session must:

1. Recover interrupted verification run: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`). Confirm `.verify_snapshot/` is removed afterward.
2. Confirm canonical state: `git log -1 --format="%H"`, `git status --short experiments/ data/ ledger/`, confirm HEAD == origin/main, confirm no `.verify_snapshot/`.
3. Run `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` to confirm goldens match pinned baseline.
4. Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items (research phase closed, E001–E043).
5. Optionally run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green — only if the user directs it.
6. If the session itself hands off, create its own timestamped durable handoff following the established pattern (`HANDOFF_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root).

Do **not** re-run verification, modify experiments, or change baselines without explicit direction. Do **not** invent new tasks, create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

## First Steps (verify state)

- Recover first: `SEED=42 python3 run_all_verification.py --restore-only`.
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

Supersedes previous INITIAL_TASK handoffs (most recent prior: `HANDOFF_2026-11-27T10-46-45Z_INITIAL_TASK.md`). This file is the authoritative initial-task message for the next session.

Handoff written by agent at 2026-11-27T10:51:43Z.