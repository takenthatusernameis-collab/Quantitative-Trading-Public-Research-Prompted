# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-07T23:00:38Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `5d6df106` (`chore(kilo): checkpoint agent session`, 2026-11-07 22:59:58 +0000)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff creation)

- `git status --short --branch`: **clean** on `main`; `HEAD == origin/main` (both `5d6df106`). No uncommitted changes.
- `.verify_snapshot/`: **absent** — no interrupted/pending verification run to recover.
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions recorded in `ledger/RESEARCH_LEDGER.md`. Ledger tail read (E105–E108) → closure confirmed; last substantive entry E108 (2026-11-07T18:16Z). No OPEN/PENDING/BLOCKED/TODO research items.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts.
- Commit delta since prior handoff (E108, HEAD `01a774c6`): 50 commits, all `chore(kilo): checkpoint agent session` plus one `a4036a51 chore: capture completed workflow run diagnostics` (writes only `research_state/workflow_run_diagnostics.jsonl`). **No change to research artifacts, data, src, tests, scripts, or ledger substance.** Baseline intact.

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
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
SEED=42 python3 run_all_verification.py              # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended   # quick + 18 committed drivers (~21 min)
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template/manual maintainer path: `.github/workflow-templates/verification-gate.yml`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.

## Symlink Tree State (repointed this session)

- 33 broken/missing symlinks repaired (28 in root, 18 in `.kilo/`, plus others) plus stale-target canonical pointers — all repointed to this artifact.
- Per-directory relative targets: root → bare filename; `handoff/` → bare filename; `.handoff/` and `.kilo/` → `../handoff/...`; `.kilo/handoff/` → `../../handoff/...`.
- Historical timestamped-named pointers (e.g. `HANDOFF_NEXT_SESSION_2026-11-07T16-37-56Z.md`) left untouched to preserve history.

## Handoff Provenance

- **Supersedes (operationally):** `handoff_2026-11-07T22-58-21Z_INITIAL_TASK.md`, `handoff_2026-11-07T22-25-49Z_INITIAL_TASK.md`, `handoff_2026-11-07T22-22-03Z_INITIAL_TASK.md`, `handoff_2026-11-07T22-21-03Z_INITIAL_TASK.md`, `handoff_2026-11-07T22-18-06Z_INITIAL_TASK.md`, `handoff_2026-11-07T22-17-13Z_INITIAL_TASK.md`, `handoff_2026-11-07T22-15-40Z_INITIAL_TASK.md`, and all earlier timestamped handoffs (retained as history).
- **Durable artifact(s):** `handoff_2026-11-07T23-00-38Z_INITIAL_TASK.md` (root), mirrored to `handoff/`, `.handoff/`, and `.kilo/handoff/` (identical content).
- **Canonical pointers:** `HANDOFF.md`, `HANDOFF_LATEST.md`, `handoff_LATEST.md`, `next_session.md`, `INITIAL_TASK.md`, `INITIAL_TASK_HANDOFF.md`, `LATEST.md`, `CURRENT.md`, `NEXT_HANDOFF.md`, `NEXT_SESSION.md`, `next_handoff.md`, `handoff_next.md`, `handoff_next_session.md`, `next_session_HANDOFF.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md`, `HANDOFF_CURRENT.md`, `HANDOFF_LATEST_INITIAL_TASK.md`, `handoff_LATEST_INITIAL_TASK.md`, `LATEST_INITIAL_TASK.md`, `INITIAL_TASK_LATEST.md`, `INITIAL_TASK_HANDOFF`, `NEXT_HANDOFF`, `HANDOFF`, `HANDOFF_CURRENT`, `HANDOFF_NEXT`, `HANDOFF_NEXT_SESSION`, `HANDOFF_NEXT_SESSION_LATEST`, `HANDOFF_LATEST`, `LATEST`, `INITIAL_TASK`, `INITIAL_TASK_LATEST`, `next_session`, `next_session_handoff`, `next_session_HANDOFF`, `handoff`, `handoff_current`, `handoff_latest`, `handoff_next`, `handoff_next_session`, `handoff_LATEST`, `handoff__INITIAL_TASK`, `handoff_next_session_LATEST`, plus all `.handoff/` and `.kilo/` and `.kilo/handoff/` equivalents.