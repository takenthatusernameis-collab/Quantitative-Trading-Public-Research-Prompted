# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T03:03:25Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `cea50f0413929183d221cdb9ca8788251e2dc4a0` (`chore(kilo): checkpoint agent session`, 2026-11-08 02:16:03 +0000)
**Remote:** `origin/main` in sync (at handoff creation)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status`: **clean** (`## main...origin/main`, no uncommitted changes).
- `.verify_snapshot/`: **absent** (no interrupted verification restore pending).
- Golden artifact check (`scripts/check_goldens_clean.py`): **ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD**.
- Canonical baselines remain authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions/history in `ledger/RESEARCH_LEDGER.md`.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and note `HEAD` vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output**. Restore goldens after any interrupted run. If `scripts/check.sh` reports a golden/baseline mismatch, fix/restore before committing.

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.

## Handoff Provenance

- **Durable artifacts (this session):** `handoff/HANDOFF_NEXT_SESSION_2026-11-08T03-03-25Z.md`, `.handoff/handoff_2026-11-08T03-03-25Z_INITIAL_TASK.md`.
- **Supersedes (operationally):** `handoff/HANDOFF_NEXT_SESSION_2026-11-08T01-12-41Z.md`, `.handoff/handoff_2026-11-08T02-15-39Z_INITIAL_TASK.md` (and earlier timestamped handoffs, retained as history).
