# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-07T19:12:18Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `7c5ded611959dcb7b47c1b5d377c3c46169b4ea3` (`chore(kilo): checkpoint agent session`, 2026-11-07 19:12:09 +0000)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff creation)

- `git status --short --branch`: **clean** on `main`; `HEAD == origin/main` (`7c5ded61`). No uncommitted changes other than this handoff file and its canonical symlink repoints (left in the working tree; not committed).
- `.verify_snapshot/`: **absent** — no interrupted/pending verification run to recover.
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions recorded in `ledger/RESEARCH_LEDGER.md`. No OPEN/PENDING/BLOCKED/TODO research items implied.
- Closed/resolved: **do not reopen** E049/E050 or E041/E042 residual ill-conditioned QP drift; **do not re-pin** E041/E042 artifacts.
- Symlink tree: canonical pointers repointed to this artifact (see Handoff Provenance).

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and note HEAD vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands; **never commit verification output**. Restore goldens after any interrupted run.

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                        # fast guards (~seconds, offline)
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
```

## Guardrails

- Never commit driver verification output over canonical goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template/manual maintainer path: `.github/workflow-templates/verification-gate.yml`).
- Do not change pre-registered gates, sensitivity grids, or outcomes without explicit justification and a ledger update.

## Handoff Provenance

- **Supersedes:** `handoff_2026-11-07T19-11-29Z_INITIAL_TASK.md` and all prior timestamped handoffs.
- **Durable copy:** repo root (`handoff_2026-11-07T19-12-18Z_INITIAL_TASK.md`).
- **Canonical pointers:** `handoff_next_session.md`, `initial_task.md`, `handoff_LATEST_INITIAL_TASK.md`, `handoff_latest.md`, `handoff_LATEST.md`, `handoff_next.md`, `next_session.md`, `handoff_current.md`, `next_handoff.md`, `handoff_next_session_INITIAL_TASK.md`, and `handoff_LATEST*`/`next_session*` aliases point to this artifact.
