# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T03:40:06Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD (at handoff creation):** `main` @ `48ecec0d052691b2032b385ff4bd9e20e7620fb6` (`chore(kilo): checkpoint agent session`)
**Remote:** `origin/main` — in sync (`## main...origin/main`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- **Research phase complete (E001–E043).** Dispositions/evidence are authoritative in `ledger/RESEARCH_LEDGER.md`. Repository is in closed, handoff-only state.
- **Canonical baselines are authoritative:** `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and pinned `data/` / `data/fundamentals/` snapshots/vintages. **Do not modify or re-pin as a side effect of routine verification.**
- **Working tree (observed):** only modified `__pycache__/*.pyc` files under `scripts/`, `src/`, and `tests/` (build artifacts, no research substance). No staged changes. No substantive diffs in `experiments/`, `data/`, `ledger/`, `scripts/`, `src/`, or `tests/`. `.verify_snapshot/` absent (no interrupted verification run).
- **Closed — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin E041/E042** to silence drift.
- **Delta vs prior durable handoff** (`handoff/handoff_2026-11-10T03-38-53Z_INITIAL_TASK.md`): HEAD unchanged at creation context except checkpoint history; no substantive research, baseline, or code changes introduced by this handoff.

## Initial Task for Next Session (CLEAR)

**Default action: WAIT for explicit user instructions.**
Do not invent experiments, run verification unprompted, change gates/outcomes/dispositions, or modify golden/baseline artifacts without explicit direction.

### 1) Verify repository state first
```bash
git status --short --branch
git log -5 --oneline
ls -la .verify_snapshot 2>/dev/null || true
python3 -m pip install -r requirements.txt   # if deps missing
SEED=42 bash scripts/check.sh
```
- If golden mismatches are reported, **restore/fix before committing**. Never checkpoint verification output over canonical goldens.
- If a stale/interrupted verification snapshot exists:
  ```bash
  SEED=42 python3 run_all_verification.py --restore-only
  ```

### 2) If the user explicitly requests verification
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # if requested (~21 min)
SEED=42 python3 run_all_verification.py --full       # if requested (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
```
- **Never commit verification output** over `experiments/*.json`. If interrupted, restore goldens before committing.
- Treat extended E041 numeric drift as known/closed context unless user explicitly asks to investigate; do not re-pin to silence drift.

### 3) If the user explicitly requests new work
- Keep changes minimal and scoped to the request.
- Preserve pre-registered gates/sensitivity/falsification discipline and multiple-testing rules (sensitivity grids are reported, not gated; promotion requires a dedicated pre-registered confirmatory run + full placebo).
- Record negative results honestly in `ledger/RESEARCH_LEDGER.md` when applicable.
- Before committing substantive changes: `SEED=42 bash scripts/check.sh`.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not create `.github/workflows/` CI gates as an automated agent (template only: `.github/workflow-templates/verification-gate.yml`; maintainer/UI action required).

## Guardrails

- **SEED=42** for reproducibility/verification runs.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not re-pin E041/E042 or golden/data baselines to silence drift/output differences.
- Do not change pre-registered gates, outcomes, or dispositions without explicit justification and a ledger update.
- Historical timestamped handoff files remain as history; canonical latest/next/current/initial-task pointers should reference this artifact.

## Handoff Provenance

- **Supersedes (operationally):** `handoff/handoff_2026-11-10T03-38-53Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- **Durable artifact:** `handoff/handoff_2026-11-10T03-40-06Z_INITIAL_TASK.md`
- **Canonical pointers updated:** root and conventional `handoff_*latest*`, `handoff_*next*`, `handoff_*current*`, `next_session*`, `next_handoff*`, and `initial_task*` aliases (where present) repointed to this artifact.
