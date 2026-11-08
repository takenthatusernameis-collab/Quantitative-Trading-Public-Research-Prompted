# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T02:15:39Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `11bd62c6c128bd2843af03b54c78d2ecef6f1af5` (`chore(kilo): checkpoint agent session`, 2026-11-08)
**Remote:** `origin/main` at same SHA (in sync at handoff time)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state:** clean working tree at handoff creation; `.verify_snapshot/` **absent** (no interrupted verification run).

## Current State (verified)

- Canonical baselines are authoritative: tracked `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions recorded in `ledger/RESEARCH_LEDGER.md`. Ledger closure through **E109** indicates no open research items.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts.
- Delta since prior durable handoff (`handoff_2026-11-08T02-07-04Z_INITIAL_TASK.md`, HEAD `1ef07a7f`): HEAD advanced to `11bd62c6` via checkpoint commit only. No research/artifact/code changes observed at handoff time; working tree clean.

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

## Handoff Provenance

- **Supersedes (operationally):** `handoff_2026-11-08T02-07-04Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).
- **Durable artifacts (identical content):** `handoff_2026-11-08T02-15-39Z_INITIAL_TASK.md` (root), `handoff/handoff_2026-11-08T02-15-39Z_INITIAL_TASK.md`, `.handoff/handoff_2026-11-08T02-15-39Z_INITIAL_TASK.md`, `.kilo/handoff/handoff_2026-11-08T02-15-39Z_INITIAL_TASK.md`.
- **Canonical pointers:** generic root `handoff_*`/`next_*`/`initial_task*` symlinks updated to target this artifact.

(End of file)
