# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T22:28:05Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD (at handoff creation):** `main` @ `f4e3d3e5f19be12c21152a39cc16ef304dae75d4` (`chore(kilo): checkpoint agent session`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (observed):** `main...origin/main` — working tree fully clean after restoring 11 tracked `__pycache__/*.pyc` bytecode artifacts that had drifted (gitignored dir, but files force-tracked). Core research areas (`experiments/`, `data/`, `ledger/`, `scripts/`, `src/`, `tests/`) have no substantive diffs from HEAD. `.verify_snapshot/` absent (no interrupted verification run detected).

---

## Current State

- **Research phase complete (E001–E043).** Dispositions and evidence are authoritative in `ledger/RESEARCH_LEDGER.md`. No open research items; ledger closure entries through E113.
- **Canonical baselines are authoritative:** `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and pinned `data/` / `data/fundamentals/` snapshots/vintages. **Do not modify or re-pin as a side effect of routine verification.**
- **Closed — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin E041/E042** to silence drift.
- **Environment note (observed, not fixed):** the active Python interpreter lacks `pandas` (and the other deps in `requirements.txt`). `SEED=42 bash scripts/check.sh` therefore cannot run end-to-end here — it fails at import time (`ModuleNotFoundError: No module named 'pandas'`). This is an environment/dependency issue, **not** a repository defect; the goldens and baselines themselves are untouched and consistent. The next session must `pip install -r requirements.txt` (or use a configured interpreter) before running the verification suite.
- **This session action:** created this durable, timestamped handoff only. Restored drifted tracked bytecode artifacts to HEAD. No experiment drivers, source code, baselines, goldens, or research dispositions were changed.

---

## Initial Task for Next Session (CLEAR)

**Default action: WAIT for explicit user instructions.**
Do not invent experiments, run verification unprompted, change gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### 1) Verify repository state first
```bash
git status --short --branch
git log --oneline -5
ls -la .verify_snapshot 2>/dev/null || true
SEED=42 bash scripts/check.sh
```
- If golden mismatches are reported, **restore/fix before committing**. Never checkpoint verification output over canonical goldens.
- If a stale/interrupted verification snapshot exists:
  ```bash
  SEED=42 python3 run_all_verification.py --restore-only
  ```
- If `scripts/check.sh` fails on import (missing deps), run `pip install -r requirements.txt` first.

### 2) If the user explicitly requests verification
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py              # quick (~8 min; 8 drivers)
SEED=42 python3 run_all_verification.py --extended   # if requested (~21 min; 26 drivers)
SEED=42 python3 run_all_verification.py --full       # if requested (~15 min; E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --restore-only
```
**Never commit verification output** over `experiments/*.json`. If interrupted, restore goldens before committing.

### 3) If the user explicitly requests new work
- Keep changes minimal and scoped to the request.
- Preserve pre-registered gates/sensitivity/falsification discipline and multiple-testing rules (sensitivity grids are reported, not gated; promotion requires a dedicated pre-registered confirmatory run + full placebo).
- Record negative results honestly in the ledger when applicable.
- Before committing substantive changes: `SEED=42 bash scripts/check.sh`.
- Do not commit `__pycache__`/bytecode artifacts (they are gitignored, though a few are currently force-tracked — leave them as-is unless intentionally purging).

---

## Guardrails

- **SEED=42** for reproducibility/verification runs.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction (keep re-pin in diff).
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer/UI only).
- Do not change pre-registered gates, outcomes, or dispositions without explicit justification and a ledger update.

## Handoff Provenance

- **Supersedes (operationally):** `handoff/handoff_2026-11-08T22-24-05Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- **Durable artifact:** `handoff/handoff_2026-11-08T22-28-05Z_INITIAL_TASK.md`
- **Mirrors (identical content):** `.handoff/handoff_2026-11-08T22-28-05Z_INITIAL_TASK.md`, `.kilo/handoff/handoff_2026-11-08T22-28-05Z_INITIAL_TASK.md`, `HANDOFFS/handoff_2026-11-08T22-28-05Z_INITIAL_TASK.md` (all three mirror dirs exist).
- **Canonical pointers to update:** `handoff_LATEST*`, `handoff_latest*`, `handoff_next*`, `handoff_current*`, `next_session*`, `next_handoff*`, `initial_task*`, and conventional legacy aliases → this artifact. Historical timestamped-named pointers/files left untouched to preserve history.

(End of file - total 71 lines)