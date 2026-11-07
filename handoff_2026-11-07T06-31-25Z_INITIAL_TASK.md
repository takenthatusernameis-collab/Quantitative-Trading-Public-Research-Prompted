# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T06:31:25Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `fbcc34c` (`chore(kilo): checkpoint agent session`) == `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- **Working tree:** clean (`git status --short --branch` shows only `## main...origin/main`, no tracked file changes).
- **HEAD vs origin:** in sync (`fbcc34c` == `origin/main`).
- **Verification snapshot:** absent; no live owner. If a run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
- **Goldens / baselines:** canonical and unchanged. `experiments/*.json` are authoritative per `ledger/golden_baseline.json` and `ledger/data_baseline.json`. **Do not re-pin** as a verification side effect.
- **Research phase:** complete (E001–E043). Survivors documented in `ledger/RESEARCH_LEDGER.md`.
- **Closed (do not reopen):** E049/E050 (optimizer determinism / exact KKT enumeration). E041/E042 ill-conditioned QP residual numeric drift — do **not** re-pin artifacts to silence drift.

## Session Summary

- User requested a durable, timestamped, clear initial-task message for the next agentic work session.
- Verified repo state at handoff time: `main` at `fbcc34c`, in sync with `origin/main`, clean tree, no `.verify_snapshot/`, no live verification owner.
- HEAD advanced from the prior handoff's reported `17d0328` to `fbcc34c` (a `chore(kilo): checkpoint agent session` checkpoint commit); no experiments, code, ledgers, goldens, or data baselines were modified in this session beyond creating this handoff artifact.
- Created this fresh timestamped handoff and repointed the canonical durable handoff references to it.

## Initial Task for Next Session (CLEAR)

**Wait for explicit user instructions.** Do not invent tasks, do not re-run verification "just to be sure," and do not modify experiments, baselines, or pre-registered outcomes without explicit direction.

**If asked to do work, verify state first:**
1. `git status --short --branch` — confirm `HEAD == origin/main` (or report divergence clearly).
2. Confirm `.verify_snapshot/` is absent and no live owner exists. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing substantive changes.

**Durable handoff duty (when explicitly needed):** Create a new timestamped `handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md`, mirror to `handoff/`, `.handoff/`, `.kilo/handoff/`, and repoint canonical `*_LATEST*`, `INITIAL_TASK*`, `HANDOFF_NEXT_SESSION*`, `handoff_next*`, and `next_session*` references. Do not create extra handoffs unprompted.

## Do Not

- Do not commit verification output; restore goldens before committing after an interrupted run.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to make verification pass.
- Do not re-open closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent; use local `make check|verify|verify-full`.
- Do not change pre-registered gates, sensitivity grids, or outcomes without explicit justification and ledger update.

## Reproduction Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                        # fast guards (~seconds)
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
```

## Handoff Provenance

- **Supersedes:** `handoff_2026-11-07T06-30-29Z_INITIAL_TASK.md` (state refreshed at `2026-11-07T06:31:25Z`; HEAD `17d0328` -> `fbcc34c`, a `chore(kilo): checkpoint agent session` checkpoint commit — no substantive repo change).
- **Durable copies:** repo root, `handoff/`, `.handoff/`, `.kilo/handoff/`.
- **Canonical symlinks repointed to this artifact.**
