# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T13-21-59Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `7abb4757` (`origin/main` in sync at handoff creation)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff creation)

- `git status`: clean working tree on `main`, in sync with `origin/main`.
- `.verify_snapshot/`: absent (no interrupted/pending verification restore).
- `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`: canonical baselines — **do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (E001–E043). Validated survivors and dispositions are recorded in `ledger/RESEARCH_LEDGER.md`.
- Closed/resolved items: **do not reopen** E049/E050 or the E041/E042 residual QP drift discussion; do not re-pin E041/E042 artifacts to silence drift.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent new experiments, re-run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

If the user requests work, first verify repository state:
1. `git status --short --branch` — confirm clean and `HEAD == origin/main` (or explain divergence).
2. Confirm `.verify_snapshot/` is absent. If a stale snapshot exists, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens as appropriate) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

If asked to run verification, use the standard commands and **never commit verification output**; restore goldens after any interrupted run.

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py
```

## Guardrails

- Never commit driver verification output over canonical goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional instruction to re-baseline.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use the template/manual maintainer path per repo docs).

## Handoff Provenance

- Supersedes: `handoff_2026-11-07T12-33-59Z_INITIAL_TASK.md`.
- Durable copies placed in repo root, `handoff/`, `.handoff/`, and `.kilo/handoff/` (where present), with `*_LATEST*` symlinks updated to this file.
