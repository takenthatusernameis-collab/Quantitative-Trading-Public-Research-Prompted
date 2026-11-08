# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T13:53:24Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `97f1c61df6d5511629d6dc0ddb99bdd7c5c9fc81` (`chore(kilo): checkpoint agent session`)
**Remote:** `origin/main` — in sync (verify with `git status --short --branch`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (at handoff creation):** working tree clean. `.verify_snapshot/` absent.

---

## Current State

- This session performed no technical research work. Created this durable, timestamped handoff only.
- Research phase complete (E001–E043); see `ledger/RESEARCH_LEDGER.md`. No open research items.
- Canonical baselines remain authoritative; do not modify or re-pin as a side effect of routine verification.
- Closed — do not reopen: E049/E050; E041/E042 residual ill-conditioned QP drift. Do not re-pin E041/E042.
- Delta since prior handoff (`handoff_2026-11-08T13-52-31Z_INITIAL_TASK.md`, HEAD `cfedb27c`): HEAD advanced via checkpoint commit `97f1c61d`. Diff is handoff/checkpoint maintenance only.

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm branch/state; working tree should be clean.
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
```

---

## Guardrails

- `SEED=42` for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens.
- Never re-pin golden/data baselines without explicit re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent.
- Do not change pre-registered gates/sensitivity grids/falsification expectations/outcomes without justification and ledger update.

---

## Handoff Provenance

- Created 2026-11-08T13:53:24Z in response to: "Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !".
- Supersedes operationally: `handoff_2026-11-08T13-52-31Z_INITIAL_TASK.md` (earlier retained as history).
- Durable artifact: `handoff_2026-11-08T13-53-24Z_INITIAL_TASK.md` (root). Mirror to `handoff/`, `.handoff/`, `.kilo/handoff/`, `HANDOFFS/` and repoint canonical `handoff_*`/`next_*`/`initial_task*` pointers to this artifact.

(End of file)