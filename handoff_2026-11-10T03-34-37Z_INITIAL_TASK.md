# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T03:34:37Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD (at handoff creation):** `main` @ `8d8a071239d761520b64264afd24c71902e08eeb` (`chore(kilo): checkpoint agent session`)
**Remote:** `origin/main` — in sync (`git status --short --branch` → `## main...origin/main`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (observed):** working tree clean except untracked/build `__pycache__/*.pyc` under `scripts/ src/ tests/` (no research substance); no staged tracked changes. `.verify_snapshot/` absent (no interrupted verification run). No diff under `experiments/ data/ ledger/ scripts/ src/ tests/` substantive content.

---

## Current State

- **Research phase complete (E001–E043).** Dispositions/evidence are authoritative in `ledger/RESEARCH_LEDGER.md`. Repository is in a closed, handoff-only state.
- **Canonical baselines are authoritative:** `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and pinned `data/` / `data/fundamentals/` snapshots/vintages. **Do not modify or re-pin as a side effect of routine verification.**
- **Closed — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin E041/E042** to silence drift.
- **This session action:** created this durable, timestamped handoff only. No experiment drivers, source code, baselines, goldens, or research dispositions were changed.
- **Delta vs prior committed durable handoff** (`handoff_2026-11-10T02-46-12Z_INITIAL_TASK.md`, HEAD `8d8a0712`): this handoff is a refresh of the same state; no `experiments/`, `data/`, `ledger/`, `scripts/`, `src/`, or `tests/` substance changed since the prior handoff.

---

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
**Never commit verification output** over `experiments/*.json`. If interrupted, restore goldens before committing.

### 3) If the user explicitly requests new work
- Keep changes minimal and scoped to the request.
- Preserve pre-registered gates/sensitivity/falsification discipline and multiple-testing rules (sensitivity grids are reported, not gated; promotion requires a dedicated pre-registered confirmatory run + full placebo).
- Record negative results honestly in the ledger when applicable.
- Before committing substantive changes: `SEED=42 bash scripts/check.sh`.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer/UI only).

## Guardrails

- **SEED=42** for reproducibility/verification runs.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not re-pin E041/E042 or golden/data baselines to silence drift/output differences.
- Do not change pre-registered gates, outcomes, or dispositions without explicit justification and a ledger update.
- Historical timestamped handoff files/pointers are retained as history; only canonical `handoff_*latest*`/`next*`/`current`/`initial_task` aliases should be repointed to this artifact.

## Handoff Provenance

- **Supersedes (operationally):** `handoff_2026-11-10T02-46-12Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- **Durable artifact:** `handoff_2026-11-10T03-34-37Z_INITIAL_TASK.md`
- **Canonical pointers to repoint:** `handoff_LATEST*`, `handoff_latest*`, `handoff_next*`, `handoff_current*`, `next_session*`, `next_handoff*`, `initial_task*`, and conventional aliases → this artifact.

(End of file - total 74 lines)
