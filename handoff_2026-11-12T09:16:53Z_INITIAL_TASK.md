# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T09:16:53Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `2d447ac1` (`chore(kilo): checkpoint agent session`) — tracks `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff)
- **Working tree:** not clean — 12 tracked `__pycache__/*.pyc` files modified under `scripts/` and `tests/` (bytecode drift only). No source, experiment, ledger, test, or config edits observed.
- **`.verify_snapshot/`:** absent (no interrupted verification run pending).
- **Research phase:** complete (E001–E043). Authoritative dispositions/open items: `ledger/RESEARCH_LEDGER.md`.
- **Canonical baselines (authoritative, do not modify routinely):** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- **Closed/resolved (do not reopen):** E049/E050 and residual E041/E042 ill-conditioned QP drift (~1-ulp, ~1e-05); do not re-pin E041/E042 artifacts to silence drift.

## Initial task for next session (CLEAR)
**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**Before any substantive work (if requested):**
1. `git status --short --branch` — confirm HEAD/alignment. Treat tracked `__pycache__` modifications explicitly (restore/discard/commit only with explicit direction); do not let bytecode changes contaminate substantive commits.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) before other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification (use `SEED=42`):**
- `make check` / `SEED=42 bash scripts/check.sh` — fast guards (~seconds, offline)
- `SEED=42 python3 verify_convention_robustness.py` — reads JSONs, no writes
- `SEED=42 python3 run_all_verification.py` [--extended|--full] — as requested
- `SEED=42 python3 run_all_verification.py --restore-only` — recover after interruption
- **Never commit verification output** over `experiments/*.json`. If interrupted, restore goldens before committing. If guards report mismatch, fix/restore before committing — do not re-pin to silence drift.

## Guardrails
- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer template: `.github/workflow-templates/verification-gate.yml`).
- Never commit secrets/keys; never log secrets.

## Handoff provenance
- **Durable artifact (this session):** `handoff_2026-11-12T09:16:53Z_INITIAL_TASK.md` (root).
- **Supersedes operationally:** `handoff_2026-11-12T09:15:39Z_INITIAL_TASK.md` and prior `handoff_*_INITIAL_TASK.md` artifacts (retained for history).

(End of file - total 43 lines)
