# Handoff: Next Agentic Work Session
**Timestamp (UTC):** 2026-10-29T00:10:25Z
**Handoff ID:** handoff-20261029T001025Z
**From:** current session
**To:** next agentic work session

## Initial Task

Resume work from a clean, verified baseline. Do **not** guess or start new experiments without first establishing state.

### Step 1: Verify Repository State (Required)
```bash
git status
git log -1 --oneline
SEED=42 bash scripts/check.sh
```

- If `scripts/check.sh` fails due to golden/baseline issues, **stop and resolve before making changes** (see AGENTS.md "Baseline Integrity").
- If `.verify_snapshot/ACTIVE.json` exists, a verification run may be pending; recover with `SEED=42 python3 run_all_verification.py --restore-only`.

### Step 2: Load Project Context (Required)
- Read `ledger/RESEARCH_LEDGER.md` (completed E001–E043; open items E048/E049).
- Read `AGENTS.md` (conventions, seeds, golden files, reproducibility).
- Inspect `experiments/` and `data/` state.

### Step 3: Determine Next Action
- Pick the highest-priority open ledger item and confirm scope before editing.
- If clean with no explicit direction, summarize state and ask for direction (no large refactors).
- Never modify committed goldens (`experiments/*.json`) as a side effect of verification; re-pin only via `python3 scripts/check_golden_baseline.py --update` with explicit justification.

## Constraints & Reminders
- Always use `SEED=42`.
- Follow pre-registration, multiple-testing discipline, falsification expectations.
- Do not commit verification outputs; restore goldens if interrupted.
- Cache coverage enforced; missing pinned data fails in offline mode.
- Optimizer determinism (E049): solver exit status is not a gating criterion; E041/E042 grids still show numeric drift beyond 1e-4 (do not re-pin to silence).

## Suggested First Action
Run Step 1, report baseline status, then propose next steps from ledger state.
