# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T12-33-59Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `f1a8228f` (`origin/main` in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- Working tree clean at handoff creation. HEAD f1a8228f == origin/main.
- Verification snapshot absent; no live verification owner.
- Goldens/baselines canonical and authoritative; do not re-pin as side effect of verification.
- Research phase complete (E001–E043); survivors in ledger/RESEARCH_LEDGER.md.
- Closed items (do not reopen): E049/E050, E041/E042 residual QP drift (do not re-pin).

## Initial Task for Next Session (CLEAR)

Wait for explicit user instructions. Do not invent tasks, re-run verification unprompted, or modify experiments/baselines/gates/outcomes without direction.

If asked to do work, verify state first:
1. `git status --short --branch` — confirm clean and HEAD == origin/main.
2. Confirm `.verify_snapshot/` absent; if stale, `SEED=42 python3 run_all_verification.py --restore-only`.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing substantive changes.

## Do Not

- Do not commit verification output; restore goldens after interrupted run.
- Do not re-pin ledger/golden_baseline.json or ledger/data_baseline.json.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create .github/workflows/ CI gates as automated agent.

## Reproduction Commands (only if requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py
```

## Handoff Provenance

- Supersedes: `handoff_2026-11-07T12-32-47Z_INITIAL_TASK.md`
- Durable copies: repo root, `handoff/`, `.handoff/`, `.kilo/handoff/`.
