# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T18:38:10Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `84f05ec7cc5cb6913a96182ec96c1aa7b3e01cd0` (2026-11-08 18:38:02 +0000), in sync with `origin/main`
**Remote:** `origin` — verify with `git status --short --branch` before work
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (at handoff creation):** working tree clean aside from this untracked handoff file and repointed handoff symlinks. `.verify_snapshot/` absent (no live/interrupted verification run).

---

## Current State

- This session performed no technical research work. It created this durable, timestamped handoff as the clear initial task message for the next agentic work session.
- Research phase complete (E001–E043); dispositions are in `ledger/RESEARCH_LEDGER.md`. No open research items.
- Canonical baselines remain authoritative; do not modify or re-pin as a side effect of routine verification.
- Closed — do not reopen: E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin E041/E042.**
- Delta since prior handoff (`handoff_2026-11-08T17-43-22Z_INITIAL_TASK.md`, HEAD `580c24d9` -> now `84f05ec7` checkpoint): no code, experiment, baseline, or research-state changes beyond the checkpoint commit. This handoff supersedes prior handoffs operationally.

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
**Never commit verification output** over canonical goldens (`experiments/*.json`). If a run is interrupted, restore goldens before committing.

---

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction (keep the re-pin in the diff).
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer/UI only).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Do not commit `__pycache__`/bytecode artifacts.

## Handoff Provenance

- **Supersedes (operationally):** `handoff_2026-11-08T17-43-22Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- **Durable artifact (this file):** `handoff_2026-11-08T18-38-10Z_INITIAL_TASK.md`
- **Canonical pointers (root, repointed to this artifact):** `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_LATEST.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md`, `CURRENT.md`, `INITIAL_TASK.md`, `LATEST.md`, `NEXT_HANDOFF.md`, `NEXT_SESSION_HANDOFF.md`, `initial_task.md`, `next_session.md`, `next_handoff.md`, `handoff_LATEST.md`, `handoff_latest.md`, `handoff_current.md`, `handoff_next.md`, `handoff_next_session.md`, and their `.md.md` / no-suffix variants where present.
