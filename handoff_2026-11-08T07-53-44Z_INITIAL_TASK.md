# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T07:53:44Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `db8917904057dcc890f479754fd6a585ca66bb9f` (`chore(kilo): checkpoint agent session`, 2026-11-08 07:51:00 +0000)
**Remote:** `origin/main` == local `HEAD` (`db891790`) at handoff creation.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state:** clean working tree at handoff creation (no tracked modifications). `.verify_snapshot/` absent. This session created this durable handoff only; **do not commit new/untracked handoff files without explicit instruction**.

---

## Current State (verified)

- No technical research work was performed in this session. No verification run, no experiment, no code change, no golden/baseline/ledger modification.
- Canonical baselines remain authoritative: tracked `experiments/*.json` goldens (138 artifacts), `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E110**; see `ledger/RESEARCH_LEDGER.md`). Last ledger entry: **E110** (HEAD `c9c61a45`, 2026-11-08T04:17Z). No open research items. No OPEN/PENDING/BLOCKED/TODO markers in the ledger.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.
- Delta since prior durable handoff (`handoff_2026-11-08T07-52-23Z_INITIAL_TASK.md`, HEAD `db891790`): HEAD unchanged; no research/artifact/code/ledger substance changed.

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm state; note untracked handoff files (do not commit unless explicitly instructed). Do not commit tracked `__pycache__/*.pyc` recompilation artifacts unless explicitly instructed.
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

- Created by this agentic session at **2026-11-08T07:53:44Z** in response to the explicit request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*.
- Supersedes (operationally): `handoff_2026-11-08T07-52-23Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- Durable artifacts (identical content): root `handoff_2026-11-08T07-53-44Z_INITIAL_TASK.md` and mirrors in `handoff/`, `.handoff/`, `.kilo/handoff/`, `HANDOFFS/`.
- Canonical pointers updated: root/handoff generic `*LATEST*`/`*next*`/`INITIAL_TASK*` handoff symlinks repointed to this artifact.

(End of file)
