# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T18:40:26Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `ddeed17dd1a8e2d2f358095f98d6ef850bef7540` (2026-11-08 18:40:07 +0000), in sync with `origin/main`
**Remote:** `origin` — verify with `git status --short --branch` before work
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (at handoff creation):** working tree clean aside from this untracked handoff file and repointed handoff symlinks. `.verify_snapshot/` absent (no live/interrupted verification run).

---

## Current State

- This session performed no technical research work. It created this durable, timestamped handoff as the clear initial task message for the next agentic work session.
- Research phase complete (E001–E043); dispositions are in `ledger/RESEARCH_LEDGER.md`. No open research items.
- Canonical baselines remain authoritative; do not modify or re-pin as a side effect of routine verification.
- Closed — do not reopen: E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin E041/E042.**
- Delta since prior handoff (`handoff_2026-11-08T18-39-04Z_INITIAL_TASK.md`, HEAD `84f05ec7`): checkpoint commits only; no code, experiment, baseline, or research-state changes. This handoff supersedes prior handoffs operationally.

---

## Initial Task for Next Session (CLEAR)

**Default action: WAIT for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm branch/state and remote sync.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before other work.
3. If `SEED=42 bash scripts/check.sh` (or `make check`) reports golden mismatches, fix/restore before committing — never checkpoint verification output over canonical goldens.
4. Before committing any substantive change: run `SEED=42 bash scripts/check.sh`.

**If asked to run verification (only when explicitly requested):**
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py              # quick
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```
