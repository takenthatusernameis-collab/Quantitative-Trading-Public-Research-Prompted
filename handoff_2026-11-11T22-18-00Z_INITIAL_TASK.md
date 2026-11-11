# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-11T22:18:00Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `44e38f89` — tracking `origin/main` (in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: `## main...origin/main` at handoff start (untracked: this handoff file only). Pre-existing tracked `__pycache__/*.pyc` modifications may be present in the worktree in some environments — **do not commit** them unless explicitly instructed.
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- Research phase complete (E001–E043). Canonical dispositions/history: `ledger/RESEARCH_LEDGER.md`.
- Golden/baseline artifacts are authoritative: `experiments/*.json` (pinned), `ledger/golden_baseline.json`, `ledger/data_baseline.json`. Pinned data inputs per `data/vintages.json` and `data/fundamentals_vintages.json`.
- Closed/resolved — **do not reopen**: E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). **Do not re-pin** E041/E042 artifacts to silence drift.

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm HEAD/remote alignment and note any pre-existing tracked `__pycache__` modifications (do not commit them).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output** over `experiments/*.json`. Restore goldens after any interrupted run. If guards report a golden/baseline mismatch, fix/restore before committing (do not re-pin to silence drift).

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never introduce logging of secrets.
- Do not commit pre-existing tracked `__pycache__/*.pyc` working-tree modifications unless explicitly instructed.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-11T22-18-00Z_INITIAL_TASK.md` (root).
- **Supersedes (operationally):** `handoff_2026-11-11T20-21-53Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).
- **HEAD at handoff:** `44e38f89` (no research/source/artifact changes by this handoff action beyond this file).
