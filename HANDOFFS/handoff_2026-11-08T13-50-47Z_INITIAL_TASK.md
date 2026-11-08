# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T13:50:47Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `961ca67a319f77fd05237dd929560e41132b7e65` (`chore(kilo): checkpoint agent session`)
**Remote:** `origin/main` @ identical SHA — in sync
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (at handoff creation):** working tree clean. `.verify_snapshot/` absent.

---

## Current State

- This session performed no technical research work. Created this durable, timestamped handoff only.
- Research phase complete (E001–E043); see `ledger/RESEARCH_LEDGER.md`. No open research items.
- Canonical baselines remain authoritative; do not modify or re-pin as side effect of routine verification.
- Closed — do not reopen: E049/E050; E041/E042 residual ill-conditioned QP drift. Do not re-pin E041/E042.
- Delta since prior handoff (`handoff_2026-11-08T13-50-14Z_INITIAL_TASK.md`, HEAD `2ddd2397`): HEAD advanced via checkpoint commit `961ca67a`. Diff is handoff/checkpoint maintenance only.

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm state; working tree should be clean.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before other work.
3. Run `SEED=42 bash scripts/check.sh` before committing any substantive change.

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
```

---

## Guardrails

- SEED=42 for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens.
- Never re-pin golden/data baselines without explicit re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as automated agent.
- Do not change pre-registered gates/sensitivity grids/falsification expectations/outcomes without justification and ledger update.

---

## Handoff Provenance

- Created 2026-11-08T13:50:47Z in response to: "Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !".
- Supersedes operationally: `handoff_2026-11-08T13-50-14Z_INITIAL_TASK.md` (earlier retained as history).
- Durable artifact: `handoff_2026-11-08T13-50-47Z_INITIAL_TASK.md` (root); mirrored to `handoff/`, `.handoff/`, `.kilo/handoff/`, `HANDOFFS/` (identical content), with canonical pointers repointed to this artifact.

(End of file)
