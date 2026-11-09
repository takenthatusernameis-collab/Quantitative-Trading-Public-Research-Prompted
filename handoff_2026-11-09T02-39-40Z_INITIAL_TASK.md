# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-09T02:39:40Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `e97a50fd` (verify: `git log -1 --oneline`)
**Remote:** `origin/main` @ `e97a50fd` (verify: `git rev-parse --short origin/main`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state:** tracked working tree clean at handoff creation; `.verify_snapshot/` absent. This session adds only this durable handoff and updates canonical handoff aliases. No experiment drivers, source, baselines, goldens, tests, scripts, or research dispositions changed.

---

## Current State

- **Research phase complete (E001–E115).** Dispositions/evidence are authoritative in `ledger/RESEARCH_LEDGER.md`. **No open research items.**
- **Canonical baselines are authoritative:** `experiments/*.json` goldens (tracked), `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` / `data/fundamentals/` snapshots. **Do not modify or re-pin as a side effect of routine verification.**
- **Closed — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin E041/E042** to silence drift.
- **Delta vs prior durable handoff** (`handoff_2026-11-09T02-37-59Z_INITIAL_TASK.md`): HEAD advanced by checkpoint commits (`32792fe0`, `db6bedbf`, `838b5e2e`, `e97a50fd`) with no substantive research changes reported; only this new handoff + alias updates added.

---

## Initial Task for Next Session (CLEAR)

**Default action: WAIT for explicit user instructions.**
Do not invent experiments, run verification unprompted, change gates/outcomes/dispositions, or modify golden/baseline artifacts without explicit direction.

### 1) Verify repository state first
```bash
git status --short --branch
git log -5 --oneline
ls -la .verify_snapshot 2>/dev/null || true
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
SEED=42 python3 run_all_verification.py --restore-only  # if interrupted
```
**Never commit verification output** over `experiments/*.json`. Restore goldens before committing if interrupted.

### 3) If the user explicitly requests new work
- Keep changes minimal and scoped to the request.
- Preserve pre-registered gates/sensitivity/falsification discipline and multiple-testing rules (sensitivity grids reported, not gated; promotion requires a dedicated pre-registered confirmatory run + full placebo).
- Record negative results honestly in the ledger when applicable.
- Before committing substantive changes: `SEED=42 bash scripts/check.sh`.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer/UI only).

---

## Guardrails

- **SEED=42** for reproducibility/verification runs.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not re-pin E041/E042 or golden/data baselines to silence drift/output differences.
- Do not change pre-registered gates, outcomes, or dispositions without explicit justification and a ledger update.
- Historical timestamped handoff files are retained as history; only canonical alias pointers are repointed.

## Handoff Provenance

- **Supersedes (operationally):** `handoff_2026-11-09T02-37-59Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).
- **Durable artifact:** `handoff_2026-11-09T02-39-40Z_INITIAL_TASK.md`
- **Canonical aliases updated:** root + `.handoff/` `handoff_LATEST*`, `handoff_next*`, `handoff_next_session*`, `next_session*`, `next_handoff*`, `initial_task*`, `handoff_current*` where present → this artifact.
