# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T14-56-22Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `e7d18c8ac074619ffa3a934b99fa626c19dedeaa` (2026-11-04) "chore(kilo): checkpoint agent session"
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean for `experiments/` and `data/` (no live verification run; `.verify_snapshot/` absent). Handoff files themselves are not git-tracked.

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*
- Wrote durable handoff `handoff_2026-11-04T14-56-22Z_INITIAL_TASK.md` under `handoff/`, repointed root and `.kilo/handoff/` alias symlinks to it.
- Did **not** run verification, modify experiments, change baselines, or take any research action. No explicit user direction beyond the handoff request.
- Supersedes previous INITIAL_TASK handoff `handoff_2026-11-04T14-55-00Z_INITIAL_TASK.md`.

## Initial Task

**CLEAR INITIAL TASK:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, change baselines, create additional handoffs unprompted, or re-open closed items. The baseline is clean and recoverable.

If no new direction arrives, the standing safe action is a state check only:
- `git log -1 --format="%H"` and `git status --short experiments/ data/` — confirm HEAD == origin/main and canonical artifacts unmodified.
- Confirm no `.verify_snapshot/` directory exists (no interrupted run to recover).
- Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items.
- Optional: `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green — read-only, no writes.

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoff `handoff_2026-11-04T14-55-00Z_INITIAL_TASK.md`. This file is the authoritative initial-task message for the next session.
Durable copies written to: `handoff/`, root, `.kilo/handoff/` (alias symlinks updated to point here).

Handoff written by agent at 2026-11-04T14-56-22Z.

(End of file)
