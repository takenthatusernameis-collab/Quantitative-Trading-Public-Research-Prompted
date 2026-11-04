# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T09:56:15Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 8a118fba22179f92b8178d53c5e61543a38646a2 (== origin/main)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean for `experiments/` and `data/` (no live verification run; `.verify_snapshot/` absent). Handoff files themselves are not git-tracked.

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !*
- Verified repository state against live HEAD before writing: HEAD == origin/main (8a118fba22179f92b8178d53c5e61543a38646a2), working tree clean for canonical artifacts (`experiments/`, `data/`), no pending `.verify_snapshot/`.
- Supersedes previous INITIAL_TASK handoff (most recent prior: `handoff_2026-11-04T09-50-44Z_INITIAL_TASK.md`). This file is the authoritative initial-task message for the next session.
- **Discovered and fixed a defect in the handoff symlink fabric** that this session inherited: 7 symlinks were dangling (root: `handoff.md`, `handoff_LATEST_INITIAL_TASK.md`, `handoff_current.md`, `handoff_next.md`, `handoff_next_session.md`, `handoff_next_session_INITIAL_TASK.md` — all pointed at `handoff/handoff_2026-11-04T09-50-05Z_INITIAL_TASK.md`, which does not exist; `.kilo/HANDOFF_NEXT_SESSION_LATEST.md` pointed at `../handoff/handoff_2026-11-04T08-06-10Z_INITIAL_TASK.md`, which also does not exist). All 7 have been re-pointed at this file and verified to resolve. **If the next session re-points symlinks, re-check every target exists with `[ -e <target> ]` before writing — dangling symlinks silently corrupt the handoff fabric.**
- Did **not** run verification, modify experiments, change baselines, or take any research action. No explicit user direction beyond the handoff request.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must create its own timestamped durable handoff following the established pattern (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` under `handoff/`, mirrored at root and `.kilo/handoff/`, repointing all root + `.kilo/handoff/` + `handoff/` symlinks) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. The baseline is clean and recoverable. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

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

Supersedes previous INITIAL_TASK handoff (most recent prior: `handoff_2026-11-04T09-50-44Z_INITIAL_TASK.md`). This file is the authoritative initial-task message for the next session.
Durable copies written to: `handoff/`, root, `.kilo/handoff/` (symlinks updated as applicable).

Handoff written by agent at 2026-11-04T09:56:15Z.

(End of file)