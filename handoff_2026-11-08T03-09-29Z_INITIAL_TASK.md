# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T03:09:29Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `1e3ad2ebef4ba91d6ae2872880157c647c694b1f` (`chore(kilo): checkpoint agent session`)
**Remote:** `origin/main` — in sync (identical SHA, verified at handoff creation)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state:** clean working tree; `.verify_snapshot/` **absent** (no interrupted verification run to recover).

---

## Current State (verified at handoff)

- **No technical work was performed this session** — only this durable handoff was written. No verification run, no experiment, no code, no baseline, no ledger change.
- Canonical baselines are authoritative: tracked `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions recorded in `ledger/RESEARCH_LEDGER.md`. Ledger closure through **E109** (2026-11-07T23:00Z); no open research items.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts.
- Delta since prior durable handoff (`handoff_2026-11-08T03-06-57Z_INITIAL_TASK.md`, HEAD `ba629fe2`): HEAD advanced to `1e3ad2eb` via checkpoint commit(s) only. No research/artifact/code changes; working tree clean except this handoff file and the canonical symlink repoint.

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and note HEAD vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output**. Restore goldens after any interrupted run.

---

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

---

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template/manual maintainer path: `.github/workflow-templates/verification-gate.yml`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Do not create extra handoffs unprompted; the durable-handoff duty fires only on explicit request.

---

## Handoff Provenance

- Created by this agentic session at 2026-11-08T03:09:29Z in response to the explicit request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*
- **Supersedes (operationally):** `handoff_2026-11-08T03-06-57Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- **Durable artifacts (identical content):** this file at root, `handoff/handoff_2026-11-08T03-09-29Z_INITIAL_TASK.md`, `.handoff/handoff_2026-11-08T03-09-29Z_INITIAL_TASK.md`, and `.kilo/handoff/handoff_2026-11-08T03-09-29Z_INITIAL_TASK.md`.
- **Canonical pointers repointed:** root, `handoff/`, `.handoff/`, and `.kilo/handoff/` generic `*_LATEST*`, `INITIAL_TASK*`, `HANDOFF*`, `next_session*`, `NEXT_*` symlinks now target this artifact using per-directory relative targets. Historical timestamped-named pointers left untouched.
