# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-08T10-42-47Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `12e0a25a` (`chore(kilo): checkpoint agent session`) == `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- **Working tree:** clean (`git status --short --branch` → `## main...origin/main`, no tracked changes).
- **HEAD vs origin:** in sync (`12e0a25a` == `origin/main`).
- **Verification snapshot:** absent; no live owner.
- **Goldens / baselines:** canonical and unchanged.
- **Research phase:** complete (E001–E043). Survivors documented in `ledger/RESEARCH_LEDGER.md`.

## Initial Task for Next Session (CLEAR)

**Wait for explicit user instructions.** Do not invent tasks, do not re-run verification "just to be sure," and do not modify experiments, baselines, or pre-registered outcomes without explicit direction.

**If asked to do work, verify state first:**
1. `git status --short --branch` — confirm `HEAD == origin/main` (or report divergence clearly).
2. Confirm `.verify_snapshot/` is absent and no live owner exists. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing substantive changes.

## Do Not

- Do not commit verification output; restore goldens before committing after an interrupted run.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to make verification pass.
- Do not re-open closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent; use local `make check|verify|verify-full`.
- Do not change pre-registered gates, sensitivity grids, or outcomes without explicit justification and ledger update.

## Reproduction Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py
```

## Handoff Provenance

- **Supersedes:** `handoff_2026-11-08T10-40-32Z_INITIAL_TASK.md`.
- **Durable copies:** repo root, `handoff/`, `.handoff/`, `.kilo/handoff/`.
- **Canonical symlinks repointed to this artifact.**

(End of file)
