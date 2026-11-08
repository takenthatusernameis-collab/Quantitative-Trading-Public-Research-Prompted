# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-08T11:50:51Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Branch:** `main` (tracking `origin/main`)
**HEAD:** `406fe20a` (`chore(kilo): checkpoint agent session`) — `main` and `origin/main` point to the same commit at handoff creation; confirm with `git status --short --branch` before acting.
**Snapshot:** `.verify_snapshot/` absent at handoff creation. No live verification owner.

## Clear Initial Task

**Wait for explicit user instructions.** This repository is in completed research/maintenance state (E001–E043; survivors documented in `ledger/RESEARCH_LEDGER.md`). Do not invent tasks, do not re-run verification speculatively, and do not modify experiments, goldens, baselines, or pre-registered outcomes without explicit direction.

## If the user assigns work, do this first

1. `git status --short --branch` — report exact branch/HEAD/divergence and any dirty state.
2. Confirm `.verify_snapshot/` is absent and no live verification owner exists. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
3. Read `AGENTS.md` and the relevant ledger entries before changing behavior.
4. For substantive changes, run `SEED=42 bash scripts/check.sh` (or `make check`) before committing.

## Guardrails (do not violate)

- **Never commit verification output.** If a run is interrupted, restore goldens first (`--restore-only` or `git checkout -- experiments/` only when safe relative to pinned baseline).
- **Never re-pin** `ledger/golden_baseline.json` or `ledger/data_baseline.json` just to make verification pass.
- **Do not re-open** closed E049/E050 or E041/E042 drift items.
- **Do not create** `.github/workflows/` CI gates as an automated agent (controller/token constraints); use local `make check|verify|verify-full`.
- **Do not move goalposts:** preserve pre-registered gates, sensitivity-grid discipline, and recorded dispositions.

## Reproduction commands (only when explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py
```

## Provenance

- **Supersedes:** `handoff_2026-11-08T10-51-49Z_INITIAL_TASK.md`.
- **Durable copies:** repo root, `handoff/`, `.kilo/handoff/`.
- **Canonical symlinks updated:** `handoff_LATEST*`, `handoff_current*`, `handoff_next*`, `next_handoff*`, `next_session*`, `initial_task*` (where present) point to this file.

(End of file - total 46 lines)