# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T03:11:43Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `3f991faa212348612303a1072529c2c02c749f78`
**Remote:** `origin/main` — in sync
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state:** clean except `__pycache__` bytecode artifacts; `.verify_snapshot/` absent.

---

## Current State (verified at handoff)

- No technical work performed this session beyond writing this durable handoff.
- Canonical baselines authoritative; do not modify/re-pin as side effect.
- Research phase complete (E001–E043); ledger closure through E109. No open research items.
- Closed/resolved — do not reopen: E049/E050; E041/E042 residual QP drift. Do not re-pin E041/E042.

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and note HEAD vs `origin/main`.
2. Confirm `.verify_snapshot/` absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before other work.
3. Run `SEED=42 bash scripts/check.sh` before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; never commit verification output. Restore goldens after any interrupted run.

---

## Reproduction / Verification Commands (only if explicitly requested)

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
- Never re-pin ledger baselines without explicit re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as automated agent.
- Do not create extra handoffs unprompted.

---

## Handoff Provenance

- Created at 2026-11-08T03:11:43Z in response to explicit request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*
- Supersedes operationally: `handoff_2026-11-08T03-09-29Z_INITIAL_TASK.md`.
(End of file)
"