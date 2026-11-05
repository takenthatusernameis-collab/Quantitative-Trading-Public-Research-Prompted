# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-05T00-17-48Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — f63289d320f9036ad06107283a79a8953af90362 (2026-11-05 00:17:39 +0000) "chore(kilo): checkpoint agent session"
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean for experiments/ and data/ (no live verification run; .verify_snapshot/ absent). Handoff files themselves are not git-tracked.

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*
- Did **not** run verification, modify experiments, change baselines, or take any research action. No explicit user direction beyond the handoff request.
- Supersedes previous INITIAL_TASK handoffs (most recent prior: handoff_2026-11-04T20-27-06Z_INITIAL_TASK.md).

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must create its own timestamped durable handoff following the established pattern (handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md under handoff/, mirrored at root and .kilo/handoff/, repointing all root + .kilo/handoff/ + handoff/ symlinks) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

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

- Created: 2026-11-05T00-17-48Z
- Supersedes: handoff_2026-11-04T20-27-06Z_INITIAL_TASK.md
- Durable locations: `handoff/handoff_2026-11-05T00-17-48Z_INITIAL_TASK.md`, mirrored at repo root and `.kilo/handoff/`.
