# INITIAL TASK - Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-06T20-02-25Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `4356913aae82bae84062528cd8baff18d72adf4e`
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Working Tree:** clean. No live verification run. `.verify_snapshot/` absent.

## Session Summary

- User request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*
- Verified repository state: working tree clean, no golden/data/ledger diffs, no interrupted verification run.
- Created durable timestamped handoff for next agent session. No modifications made to codebase, experiments, or baselines.

## Initial Task

**CLEAR INITIAL TASK:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. Do not invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items.

## Guardrails

- Research phase complete (E001–E043 committed; E044–E050 closed). Do not re-run/re-open completed research without explicit pre-registration as E051+.
- Never modify `experiments/*.json` goldens without going through proper baseline update process.
- Never re-pin baselines to silence drift.
- Always use `SEED=42`. Close-to-close is primary convention.
- Validate optimizer on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- `experiments/` are committed goldens — verification backs up and restores them.
- Do not commit unless explicitly requested.
- Baseline integrity: `ledger/golden_baseline.json` and `ledger/data_baseline.json` are authoritative pins.

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Verification Commands (if explicitly asked to reproduce)

- `SEED=42 bash scripts/check.sh` (fast)
- `SEED=42 python3 run_all_verification.py` (quick)
- `SEED=42 python3 run_all_verification.py --extended`
- `SEED=42 python3 run_all_verification.py --full`
- `SEED=42 python3 run_all_verification.py --restore-only` (recover after interrupted run)

## Key References

- `AGENTS.md` — project commands, conventions, reproducibility, baseline integrity, CI/automation.
- `ledger/RESEARCH_LEDGER.md` — research history and surviving strategies.
- `ledger/golden_baseline.json` — SHA-256 fingerprint of canonical `experiments/` artifacts.
- `ledger/data_baseline.json` — pinned data-cache coverage.
- `run_all_verification.py` — verification suite.

## Handoff Provenance

- Created: 2026-11-06T20-02-25Z
- Durable location: handoff/handoff_2026-11-06T20-02-25Z_INITIAL_TASK.md
