# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-24T02:07:58Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 442d398393bc9a91498e675e9344e87bda69dc97 (2026-11-24 01:06:47 +0000)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean for canonical artifacts (`experiments/`, `data/`, `ledger/`). Only uncommitted change is tracked `src/__pycache__/cache_keys.cpython-312.pyc` build noise. No live verification run; `.verify_snapshot/` and `.verify_reports/` absent.

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*
- Verified repository state against live HEAD before writing: HEAD == `origin/main` (`git rev-list --left-right --count origin/main...HEAD` = `0  0`); `git status --short experiments/ data/ ledger/` empty; no `.verify_snapshot/` (no interrupted run to recover).
- Supersedes previous INITIAL_TASK handoffs (most recent prior: `handoff_2026-11-24T02-07-16Z_INITIAL_TASK.md` at root, mirrored in `handoff/` and `.kilo/handoff/`). This file is the authoritative initial-task message for the next session.
- Did **not** run verification, modify experiments, change baselines, or take any research action. No explicit user direction beyond the handoff request.

## CLEAR INITIAL TASK

**Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.**

The next agentic work session must create its own timestamped durable handoff following the established pattern (`HANDOFF_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root, mirrored in `handoff/` and `.kilo/handoff/`, repointing all root + `handoff/` + `.kilo/handoff/` generic aliases) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. The baseline is clean and recoverable. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

## First Steps (verify state)

- `git log -1 --format="%H"` and `git status --short experiments/ data/` — confirm HEAD == origin/main and canonical artifacts unmodified.
- Confirm no `.verify_snapshot/` directory exists (no interrupted run to recover).
- Read `ledger/RESEARCH_LEDGER.md` for the surviving validated strategies and open items (research phase closed, E001–E043; ledger extends through E729 handoff-refresh entries).
- Quick check before any change: `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green.

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json` (107 pinned artifacts); data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json` (35 pinned inputs).
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs (most recent prior: `handoff_2026-11-24T02-07-16Z_INITIAL_TASK.md`). This file is the authoritative initial-task message for the next session.
Durable copies written to: repo root, `handoff/`, `.kilo/handoff/` (symlinks updated as applicable).

Handoff written by agent at 2026-11-24T02:07:58Z.
