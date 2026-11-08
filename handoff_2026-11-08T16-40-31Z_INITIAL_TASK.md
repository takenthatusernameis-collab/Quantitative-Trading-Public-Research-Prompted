# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T16:40:31Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `f9ead724 chore(kilo): checkpoint agent session` (in sync with `origin/main`)
**Remote:** `origin/main` — verify with `git status --short --branch` before work
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (at handoff creation):** working tree clean (verified). `.verify_snapshot/` absent (no live/interrupted verification run).

---

## Current State

- This session performed no technical research work. It created this durable, timestamped handoff in response to the request to leave a clear initial task message for the next agentic work session.
- Research phase complete (E001–E043); see `ledger/RESEARCH_LEDGER.md`. No open research items.
- Canonical baselines remain authoritative; do not modify or re-pin as a side effect of routine verification.
- Closed — do not reopen: E049/E050; E041/E042 residual ill-conditioned QP drift. Do not re-pin E041/E042.
- Delta since prior handoff (`handoff_2026-11-08T16-37-47Z_INITIAL_TASK.md`, noted HEAD `f9ead724`): no code, experiment, or baseline changes. This handoff supersedes it operationally.

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm branch/state and remote sync (`main` in sync with `origin/main`).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before other work.
3. If `SEED=42 bash scripts/check.sh` reports golden mismatches, fix/restore before committing — never checkpoint verification output over canonical goldens.

**If asked to run verification:** use standard commands with `SEED=42`; never commit verification output over canonical goldens. Restore goldens after any interrupted run.

---

## Reproduction / Verification Commands (use only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the actual workflow via the GitHub UI).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.

## Handoff Provenance

- **Supersedes (operationally):** `handoff_2026-11-08T16-37-47Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- **Durable artifact (this file):** `handoff_2026-11-08T16-40-31Z_INITIAL_TASK.md`.
- **Canonical pointers repointed (root):** `handoff_LATEST`, `handoff_LATEST.md`, `handoff_LATEST_INITIAL_TASK`, `handoff_LATEST_INITIAL_TASK.md`, `next_session.md`, `next_session_INITIAL_TASK.md`, `LATEST.md`, `LATEST_INITIAL_TASK`, `LATEST_INITIAL_TASK.md` → this artifact (relative symlinks).

(End of file)
