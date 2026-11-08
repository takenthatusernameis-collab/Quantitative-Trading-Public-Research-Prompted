# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T01-13-58Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `1e0ccf21da` (`chore(kilo): checkpoint agent session`, recent)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state at handoff:** working tree clean; `main` in sync with `origin/main` as observed (re-verify with `git status --short --branch`).

## Current State (verified at handoff)

- `.verify_snapshot/`: **absent** — no interrupted/pending verification run to recover.
- Canonical baselines are authoritative: `experiments/*.json` (tracked goldens), `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions recorded in `ledger/RESEARCH_LEDGER.md`. Ledger closure through **E109** indicates no open research items.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts.
- Delta since prior handoff (`handoff_2026-11-08T01-10-37Z_INITIAL_TASK.md`, HEAD `5decc3ca`): HEAD advanced via checkpoint commits (`5decc3ca` → `04aee731` → `456f6bd7` → `1e0ccf21`). No substantive research/artifact/code changes indicated by handoff context.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and note HEAD vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands; **never commit verification output**. Restore goldens after any interrupted run.

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                        # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
SEED=42 python3 run_all_verification.py              # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended   # quick + 18 committed drivers (~21 min)
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template/manual maintainer path: `.github/workflow-templates/verification-gate.yml`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.

## Handoff Provenance

- **Supersedes (operationally):** `handoff_2026-11-08T01-10-37Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).
- **Durable artifacts (identical content):** this file at root, `handoff/handoff_2026-11-08T01-13-58Z_INITIAL_TASK.md`, `.handoff/handoff_2026-11-08T01-13-58Z_INITIAL_TASK.md`, and `.kilo/handoff/handoff_2026-11-08T01-13-58Z_INITIAL_TASK.md`.
- **Canonical pointers:** root and mirror generic `*_LATEST*`, `INITIAL_TASK*`, `HANDOFF*`, `next_session*`, `NEXT_*` pointers should target this artifact (per-directory relative targets where symlinks are used). Historical timestamped-named pointers left untouched.

(End of file)
