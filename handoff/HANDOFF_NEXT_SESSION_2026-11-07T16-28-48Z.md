# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T16:28:48Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `bd327c3f chore(kilo): checkpoint agent session` (in sync with `origin/main`; verify vs `origin/main` before work)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff creation)

- `git status --short --branch`: **clean** on `main` at handoff time; `HEAD == origin/main`.
- `.verify_snapshot/`: **absent** (no interrupted/pending verification restore).
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**). Dispositions in `ledger/RESEARCH_LEDGER.md`.
- Closed/resolved: **do not reopen** E049/E050 or E041/E042 residual ill-conditioned QP drift; **do not re-pin** E041/E042 artifacts to silence drift.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and note HEAD vs `origin/main` divergence.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands; **never commit verification output**. Restore goldens after any interrupted run.

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                        # fast guards
SEED=42 python3 run_all_verification.py              # quick
SEED=42 python3 run_all_verification.py --extended   # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
```

## Guardrails

- Never commit driver verification output over canonical goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use template/manual maintainer path per repo docs).
- Do not change pre-registered gates, sensitivity grids, or outcomes without explicit justification and a ledger update.

## Handoff Provenance

- **Supersedes (operationally):** `handoff_2026-11-07T16-28-06Z_INITIAL_TASK.md` (and earlier handoffs); those remain in place as history.
- **Durable copies:** repo root `handoff_2026-11-07T16-28-48Z_INITIAL_TASK.md`, `.handoff/`.
- **Canonical pointers updated:** `handoff_next_session.md`, `initial_task.md`, `handoff_LATEST_INITIAL_TASK.md`, `handoff_latest.md`, `handoff_LATEST.md`, `handoff_next.md`, `next_handoff.md`, `next_session.md`, `handoff_current.md` (where present) → this artifact.
