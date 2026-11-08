# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T22:36:50Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD (at handoff creation):** `main` @ `50d278308117b0fb27eeef7988ec2d29287b6b4c` (`chore(kilo): checkpoint agent session`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (observed):** `main...origin/main` in sync; working tree clean. `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/` → empty (0 files). `.verify_snapshot/` absent (no interrupted verification run). 138 tracked `experiments/*.json` goldens present at HEAD.
**Environment note (observed):** Python dependencies from `requirements.txt` may not be installed in the active interpreter; `SEED=42 bash scripts/check.sh` will fail at import time if deps are missing. Install deps before running verification.
**This session action:** created this durable, timestamped handoff only. No experiment drivers, source code, baselines, goldens, or research dispositions were changed.

---

## Current State

- **Research phase complete (E001–E043).** Dispositions/evidence are authoritative in `ledger/RESEARCH_LEDGER.md`. Repository is in a closed, handoff-only state through ledger entry **E114** (prior handoff).
- **Canonical baselines are authoritative:** `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and pinned `data/` / `data/fundamentals/` snapshots/vintages. **Do not modify or re-pin as a side effect of routine verification.**
- **Closed — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin E041/E042** to silence drift.
- **Delta vs prior handoff (E114, HEAD `aeac5fd2`):** HEAD advanced `aeac5fd2` → `50d27830` via a checkpoint commit; no changes to `experiments/`, `data/`, `ledger/`, `scripts/`, `src/`, or `tests/`. Prior closed/conformance state adopted.

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
- Historical timestamped handoff pointers/files are retained as history; only canonical `handoff_*latest*`/`next*` aliases should be repointed to this artifact.

## Handoff Provenance

- **Supersedes (operationally):** `handoff_2026-11-08T22-31-18Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- **Durable artifact:** `handoff_2026-11-08T22-36-50Z_INITIAL_TASK.md`
- **Mirrors:** `.handoff/`, `.kilo/handoff/`, `HANDOFFS/`, and `handoff/` (where present) — identical content.
- **Canonical pointers repointed:** `handoff_LATEST*`, `handoff_latest*`, `handoff_next*`, `handoff_current*`, `next_session*`, `next_handoff*`, `initial_task*`, and conventional aliases → this artifact.
