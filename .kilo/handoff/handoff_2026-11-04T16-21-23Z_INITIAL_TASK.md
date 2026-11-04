# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T16-20-57Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 1f306584b64d4a07532fe8ad7b9bfbdd235859af
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean

## Session Summary

- User requested: "Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"
- Captured current repo state (HEAD, clean tree, no interrupted verification).
- Created timestamped durable handoff under `handoff/` and mirrored to `.kilo/handoff/`.
- No research actions taken.

## Initial Task

**CLEAR INITIAL TASK:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, change baselines, or make changes.

If explicit direction is given, follow AGENTS.md strictly. Otherwise, state is ready - no pending work.

## Key Constraints (from AGENTS.md)
- `experiments/*.json` are committed goldens - verification backs up/restores them; never commit verification output
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`
- Data coverage enforced by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`
- Optimizer validates on constraints not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049)
- Always use `SEED=42`. Close-to-close is primary convention.
- CI workflow cannot be created by agents - use local `make check/verify/*`
- Never re-pin artifacts to silence drift without following the process

## Provenance
- Captured at: 2026-11-04T16-20-57Z
- HEAD: 1f306584b64d4a07532fe8ad7b9bfbdd235859af
- git status: clean
- experiments/: unmodified vs HEAD
- .verify_snapshot/: none

**This handoff supersedes previous INITIAL_TASK handoffs.**
