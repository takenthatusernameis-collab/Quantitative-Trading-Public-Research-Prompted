# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-07T18-10-26Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `a10615bc9451a04a1a7c1055644a32760856c24f` (`chore(kilo): checkpoint agent session`, 2026-11-07 17:21:51 +0000)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff creation)

- `git status --short --branch`: **clean** on `main` (no uncommitted source/baseline changes observed before writing this handoff).
- `.verify_snapshot/`: **absent** — no interrupted/pending verification run to recover.
- Canonical baselines remain authoritative: `experiments/*.json` (107 tracked artifacts present), `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions recorded in `ledger/RESEARCH_LEDGER.md`. No OPEN/PENDING/BLOCKED/TODO research items are implied by this handoff.
- Closed/resolved: **do not reopen** E049/E050 or E041/E042 residual ill-conditioned QP drift; **do not re-pin** E041/E042 artifacts.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and note HEAD vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands from `AGENTS.md`; **never commit verification output**. Restore goldens after any interrupted run.

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

- **Created in response to:** explicit user request to leave a timestamped clear initial task message for the next agentic work session in a durable handoff.
- **Supersedes (recent):** `handoff_2026-11-07T17-21-18Z_INITIAL_TASK.md` and prior timestamped handoffs.
- **Durable copies:** repo root (`handoff_2026-11-07T18-10-26Z_INITIAL_TASK.md`), `.handoff/`, `handoff/`, `.kilo/handoff/`.
- **Canonical pointers updated:** `handoff_next_session.md`, `initial_task.md`, `handoff_LATEST_INITIAL_TASK.md`, `handoff_latest.md`, `handoff_LATEST.md`, `handoff_next.md`, `next_session.md`, `handoff_current.md`, plus key symlinks under `.handoff/`, `handoff/`, and `.kilo/handoff/` pointing to this file.
