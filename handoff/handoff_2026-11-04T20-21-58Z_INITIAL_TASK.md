# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T20:21:58Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main (see `git log -1`)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Session Summary

- Responded to user request: "Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"
- No research actions taken; baseline left untouched.

## Initial Task

**CLEAR INITIAL TASK:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, change baselines, create additional handoffs unprompted, or re-open closed items.

If no new direction arrives, perform state check only:
- `git log -1 --format="%H"` and `git status --short experiments/ data/` — confirm HEAD == origin/main and canonical artifacts unmodified.
- Confirm no `.verify_snapshot/` directory exists.
- Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items.
- Optional: `SEED=42 bash scripts/check.sh` (read-only) to confirm goldens + data coverage + JSON guards green.

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (`tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- Never re-pin artifacts to silence drift; committed golden is authoritative record.

## Handoff provenance

State captured at 2026-11-04T20:21:58Z. This handoff supersedes previous INITIAL_TASK handoffs.

Durable copy: `handoff/handoff_2026-11-04T20-21-58Z_INITIAL_TASK.md`

(End of file)
