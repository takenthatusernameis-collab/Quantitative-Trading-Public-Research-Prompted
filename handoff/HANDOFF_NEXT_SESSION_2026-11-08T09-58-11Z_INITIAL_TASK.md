# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T09:58:11Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `4f48cabdf4649999f04915799150c0130d680f57` (`chore(kilo): checkpoint agent session`, 2026-11-08 09:57:11 +0000)
**Remote:** `origin/main` in sync with local `HEAD` at handoff creation.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state:** clean tracked state except 12 modified `__pycache__/*.pyc` recompilation artifacts (`git status --short --branch`); `.verify_snapshot/` absent (no interrupted verification run to recover). **Do not commit** new/untracked handoff files or pyc recompilation without explicit instruction.

---

## Current State (verified at handoff)

- No technical research work was performed this session — only this durable handoff was created per explicit request. No verification run, no experiment, no code change, no baseline/golden/ledger modification.
- Canonical baselines remain authoritative: tracked `experiments/*.json` goldens (expected to match HEAD unless intentionally changed), `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E110** recorded; see `ledger/RESEARCH_LEDGER.md`). Last ledger entry context: **E110** (Durable Handoff Refresh). No open research items. No OPEN/PENDING/BLOCKED/TODO markers should be introduced; do not reopen closed items.
- **Correction carried forward:** earlier handoffs incorrectly stated "E001–E043"; research runs **E001–E110**.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.
- Delta since prior durable handoff (`handoff_2026-11-08T09-56-59Z_INITIAL_TASK.md`): HEAD advanced by one checkpoint commit (`105c9195` -> `4f48cabd`); no research/artifact/code/ledger substance changed by this handoff.

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm state; note any untracked handoff files or modified tracked `__pycache__/*.pyc` recompilation artifacts (do not commit unless explicitly instructed).
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
- Do not create `.github/workflows/` CI gates as an automated agent (template/manual path: `.github/workflow-templates/verification-gate.yml`, `VERIFICATION_GATE_TEMPLATE.md`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Keep handoffs durable and factual; do not create extra handoffs unprompted beyond explicit request.

---

## Handoff Provenance

- Created by this agentic session at **2026-11-08T09:58:11Z** in response to the explicit request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*.
- Supersedes (operationally): `handoff_2026-11-08T09-56-59Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- Durable artifacts: root `handoff_2026-11-08T09-58:11Z_INITIAL_TASK.md` and mirrors in `handoff/`, `.handoff/`, `.kilo/handoff/`, `HANDOFFS/`.
- Canonical pointers updated (root): `handoff_LATEST_INITIAL_TASK`, `handoff_LATEST_INITIAL_TASK.md`, `HANDOFF_LATEST_INITIAL_TASK`, `HANDOFF_LATEST_INITIAL_TASK.md`, `LATEST_INITIAL_TASK`, `LATEST_INITIAL_TASK.md` → `handoff_2026-11-08T09:58:11Z_INITIAL_TASK.md` (symlinks where writable).
