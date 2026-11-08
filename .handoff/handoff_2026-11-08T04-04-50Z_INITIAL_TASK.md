# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T04:04:50Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `0ac742bc9e95ce68ff37375e4b809a9ea8b884a1` (`chore(kilo): checkpoint agent session`, 2026-11-08T03:17:26Z)
**Remote:** `origin/main` @ `0ac742bc...` — in sync (identical SHA verified at handoff creation)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state:** no uncommitted source/config/data changes. Only pre-existing working-tree modifications to **tracked `__pycache__/*.pyc` files** (scripts/src/tests — 12 files, 0 insertions/deletions, byte-identical recompilation). Do **not** commit these without explicit instruction. `.verify_snapshot/` **absent** (no interrupted verification run to recover).

---

## Current State (verified at handoff)

- **No technical research work was performed this session** — only this durable handoff was written (requested explicitly). No verification run, no experiment, no code change, no baseline change, no ledger change.
- Canonical baselines remain authoritative: tracked `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions recorded in `ledger/RESEARCH_LEDGER.md`. Ledger closure through **E109** (2026-11-07T23:00Z per prior handoffs); no open research items stated.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.
- Delta since prior durable handoff (`handoff_2026-11-08T03-16-11Z_INITIAL_TASK.md`): HEAD unchanged (`0ac742bc` == `origin/main`). This session adds a fresh timestamped durable handoff and canonical pointer updates only.

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm state; note the pre-existing modified tracked `__pycache__` files. Do **not** commit them unless explicitly instructed and understood.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output** over canonical goldens. Restore goldens after any interrupted run. Follow `AGENTS.md` baseline-integrity rules exactly.

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
- Do not reopen closed E049/E050 or E041/E042 drift items; do not re-pin E041/E042 to mask ill-conditioned QP drift.
- Do not create `.github/workflows/` CI gates as an automated agent (template/manual maintainer path: `.github/workflow-templates/verification-gate.yml`, `VERIFICATION_GATE_TEMPLATE.md`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Keep handoffs durable and factual; do not create extra handoffs unprompted beyond explicit request.

---

## Handoff Provenance

- Created by this agentic session at **2026-11-08T04:04:50Z** in response to the explicit request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*.
- **Supersedes (operationally):** `handoff_2026-11-08T03-16-11Z_INITIAL_TASK.md`, `handoff_2026-11-08T03-14-46Z_INITIAL_TASK.md`, `handoff_2026-11-08T03-13-00Z_INITIAL_TASK.md`, and all earlier timestamped handoffs (retained as history).
- **Durable artifacts (identical content intended):** root `handoff_2026-11-08T04-04-50Z_INITIAL_TASK.md`, `handoff/handoff_2026-11-08T04-04-50Z_INITIAL_TASK.md`, `.handoff/handoff_2026-11-08T04-04-50Z_INITIAL_TASK.md`, `.kilo/handoff/handoff_2026-11-08T04-04-50Z_INITIAL_TASK.md` (created where directories exist).
- **Canonical pointers:** repointed root and subdirectory generic `*_LATEST*`, `INITIAL_TASK*`, `HANDOFF*`, `next_session*`, `NEXT_*` symlinks to this artifact using per-directory relative targets where applicable.