# INITIAL TASK - Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-06T20:04:08Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `010096826c2bbe617f33424fa9ef772fa5d70bf6`
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Working Tree:** clean. No live verification run. `.verify_snapshot/` absent. No uncommitted diffs.

## Session Summary

- User request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !*
- Verified repository state: working tree clean, `git status --short` empty, `git diff --stat HEAD` empty, no `.verify_snapshot/` directory (no interrupted verification run in progress), HEAD matches `origin/main`.
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
- CI gate (`.github/workflows/verification-gate.yml`) cannot be created by automated agents — controller restores `.github/workflows/` at checkpoints; template at `.github/workflow-templates/verification-gate.yml`.

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Verification Commands (if explicitly asked to reproduce)

- `SEED=42 bash scripts/check.sh` (fast convention check)
- `SEED=42 python3 run_all_verification.py` (quick, ~8 min)
- `SEED=42 python3 run_all_verification.py --extended` (extended, ~21 min)
- `SEED=42 python3 run_all_verification.py --full` (full, ~15 min)
- `SEED=42 python3 run_all_verification.py --skip-slow` (convention only)
- `SEED=42 python3 run_all_verification.py --restore-only` (recover after interrupted run)

## Key References

- `AGENTS.md` — project commands, conventions, reproducibility, baseline integrity, CI/automation.
- `ledger/RESEARCH_LEDGER.md` — research history and surviving strategies.
- `ledger/golden_baseline.json` — SHA-256 fingerprint of canonical `experiments/` artifacts.
- `ledger/data_baseline.json` — pinned data-cache coverage.
- `run_all_verification.py` — verification suite.
- `scripts/check_goldens_clean.py` / `scripts/check_golden_baseline.py` — baseline integrity guards.

## Handoff Provenance

- Created: 2026-11-06T20:04:08Z
- Durable location: `handoff/handoff_2026-11-06T20-04-08Z_INITIAL_TASK.md`
- Prior handoff: `handoff/handoff_2026-11-06T20-03-12Z_INITIAL_TASK.md`
