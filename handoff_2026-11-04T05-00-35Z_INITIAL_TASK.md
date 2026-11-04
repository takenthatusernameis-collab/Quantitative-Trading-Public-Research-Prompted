# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T05-00-35Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 423dba0b96802ba60fd5b3efaf60c921872ff2fc
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** dirty. Uncommitted changes present.

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*
- Verified repository state: HEAD at 423dba0b96802ba60fd5b3efaf60c921872ff2fc vs origin/main 423dba0b96802ba60fd5b3efaf60c921872ff2fc, tracked tree clean.
- Created new timestamped handoff as requested. No research action taken — wait for explicit user direction.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must:
1. Review this handoff and the current repository state (goldens, ledger, verification guards).
2. Wait for explicit user instructions before taking any research action (re-running verification, modifying experiments, changing baselines).
3. If asked to do work, follow all constraints in AGENTS.md strictly.

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E50).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs. This file is the authoritative initial-task message for the next session.

Handoff written by agent at 2026-11-04T05:00:35Z.
