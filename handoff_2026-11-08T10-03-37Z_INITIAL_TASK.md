# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T10:03:37Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `b6b6ca2a4443a004983c48107bfadbe67023e899` (`chore(kilo): checkpoint agent session`, 2026-11-08 10:03:37 +0000)
**Remote:** `origin/main` in sync with local `HEAD` at handoff creation.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state:** clean (`git status --short --branch` shows `## main...origin/main` with no tracked changes). `.verify_snapshot/` absent (no interrupted verification run). **Do not commit** handoff artifacts or pycache changes without explicit instruction.

---

## Current State (verified at handoff)

- No research, experiment, verification, code, or baseline work was performed in this session. This durable handoff was created in response to an explicit request.
- Canonical baselines remain authoritative: tracked `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E110** recorded; see `ledger/RESEARCH_LEDGER.md`). No open research items. Do not reopen closed items.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.
- Delta since prior durable handoff (`handoff_2026-11-08T10-02-33Z_INITIAL_TASK.md`): HEAD advanced (`cb638873` → `b6b6ca2a`); no research/artifact/code/ledger substance changed by this handoff.

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean state and note HEAD vs `origin/main`.
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

- Created by this agentic session at **2026-11-08T10:03:37Z** in response to the explicit request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*.
- Supersedes (operationally): `handoff_2026-11-08T10-02-33Z_INITIAL_TASK.md` and `handoff_2026-11-08T10-01-58Z_INITIAL_TASK.md` and `handoff_2026-11-08T10-00-12Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- Durable artifacts: root `handoff_2026-11-08T10-03-37Z_INITIAL_TASK.md` and mirrors in `handoff/`, `.handoff/`, `.kilo/handoff/`, `HANDOFFS/` (where writable).
- Canonical pointers updated (root): `handoff_LATEST_INITIAL_TASK`, `handoff_LATEST_INITIAL_TASK.md`, `HANDOFF_LATEST_INITIAL_TASK`, `HANDOFF_LATEST_INITIAL_TASK.md`, `LATEST_INITIAL_TASK`, `LATEST_INITIAL_TASK.md` → `handoff_2026-11-08T10-03-37Z_INITIAL_TASK.md` (symlinks where writable).
(End of file)
