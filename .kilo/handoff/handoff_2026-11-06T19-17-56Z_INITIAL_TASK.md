# INITIAL TASK - Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-06T19:17:56Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `448e8ce7ec159fffdfe7b589716a4d42deba19c4` (`chore(kilo): checkpoint agent session`, 2026-11-06 19:17:47 +0000)
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Working Tree:** clean. No live verification run. `.verify_snapshot/` absent.

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !*
- Verified repository state against live HEAD: working tree clean, no golden/data/ledger diffs, no interrupted verification run.
- No modifications made to codebase, experiments, or baselines. Session prepared for handoff only.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must create its own timestamped durable handoff following the established pattern (`handoff/handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md`, mirrored under `.kilo/handoff/`, repointing root `handoff_LATEST_INITIAL_TASK.md` and `handoff__INITIAL_TASK.md` symlinks) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction.

**Guardrails:**
- Research phase complete (E001–E043 committed; E044–E050 closed). Do not re-run/re-open completed research without explicit pre-registration as E051+.
- Never modify `experiments/*.json` goldens without going through proper baseline update process.
- Never re-pin baselines to silence drift.
- Always use `SEED=42`. Close-to-close is primary convention.
- Validate optimizer on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- `experiments/` are committed goldens — verification backs up and restores them.
- Do not commit unless explicitly requested.

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
- `run_all_verification.py` — verification suite (`--quick` / `--extended` / `--full` / `--skip-slow` / `--restore-only`).

## Handoff Provenance

- Created: 2026-11-06T19:17:56Z
- Durable location: `handoff/handoff_2026-11-06T19-17-56Z_INITIAL_TASK.md`
- Supersedes: `handoff/handoff_2026-11-06T19-16-34Z_INITIAL_TASK.md` (HEAD `fd43166` at that time).