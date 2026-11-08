# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T18:45:14Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `a8b00bc5` (`chore(kilo): checkpoint agent session`)
**Remote:** `origin/main` (verify: `git status --short --branch`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (at handoff creation):** clean relative to research/code state; `.verify_snapshot/` absent.

---

## Current State

- Research phase complete (E001–E043). Dispositions and evidence are in `ledger/RESEARCH_LEDGER.md`. No open research items.
- Canonical baselines are authoritative: `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and pinned data/fundamentals snapshots. Do not modify or re-pin as a side effect of routine verification.
- Closed — do not reopen: E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin E041/E042.**
- This session created this durable, timestamped handoff only; no code, experiment, baseline, or research-state changes were made.

---

## Initial Task for Next Session (CLEAR)

**Default action: WAIT for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm branch/state and remote sync.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`). If golden mismatches appear, restore/fix before committing — never checkpoint verification output over canonical goldens.
4. Before committing any substantive change, run `SEED=42 bash scripts/check.sh`.

**If asked to run verification (only when explicitly requested):**
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py              # quick
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
```

**Never commit verification output** over canonical goldens (`experiments/*.json`). If interrupted, restore goldens before committing.

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

- **Supersedes (operationally):** `handoff_2026-11-08T18-44-13Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- **Durable artifact (this file):** `handoff_2026-11-08T18-45-14Z_INITIAL_TASK.md`
- **Canonical pointers (root, to be repointed):** `handoff_LATEST*`, `next_session*`, `initial_task*` and related aliases where present.
