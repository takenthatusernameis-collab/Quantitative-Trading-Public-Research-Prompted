# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T09-35-58Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `9982849` (`chore(kilo): checkpoint agent session`) == `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- **Working tree:** clean at handoff creation (`git status --short --branch` → `## main...origin/main`).
- **HEAD vs origin:** in sync (`9982849` == `origin/main`).
- **Verification snapshot:** `.verify_snapshot/` absent / no live owner detected. If a run is interrupted later: `SEED=42 python3 run_all_verification.py --restore-only`.
- **Goldens / baselines:** canonical and authoritative — `experiments/*.json` per `ledger/golden_baseline.json`; data inputs per `ledger/data_baseline.json`. **Do not re-pin** as a verification side effect.
- **Research phase:** complete (E001–E043). Survivors/decisions documented in `ledger/RESEARCH_LEDGER.md`.
- **Closed (do not reopen):** E049/E050 (optimizer determinism / exact KKT enumeration). E041/E042 residual ill-conditioned QP numeric drift — **do not re-pin artifacts** to silence drift.

## Initial Task for Next Session (CLEAR)

**Wait for explicit user instructions.** Do not invent tasks, do not re-run verification “just to be sure,” and do not modify experiments, baselines, or pre-registered outcomes without explicit direction.

**If asked to do work, verify state first:**
1. `git status --short --branch` — confirm state and `HEAD == origin/main` (report divergence clearly if present).
2. Confirm `.verify_snapshot/` is absent and no live verification owner exists. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing substantive changes.

**Durable handoff duty (only when explicitly needed):** create a new timestamped `handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md`, mirror to `handoff/`, `.handoff/`, `.kilo/handoff/`, and repoint canonical `*_LATEST*`, `INITIAL_TASK*`, `HANDOFF_NEXT_SESSION*`, `handoff_next*`, `next_session*` references. Do not create extra handoffs unprompted.

## Do Not

- Do not commit verification output; restore goldens before committing after an interrupted run.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to make verification pass.
- Do not re-open closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent; use local `make check|verify|verify-full`.
- Do not change pre-registered gates, sensitivity grids, or outcomes without explicit justification and a ledger update.

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

- **Supersedes:** `handoff_2026-11-07T09-32-02Z_INITIAL_TASK.md` (state refreshed at `2026-11-07T09-35-58Z`; HEAD `9982849`, clean tree, origin in sync).
- **Durable copies:** repo root, `handoff/`, `.handoff/`, `.kilo/handoff/`.
- **Canonical references:** `*_LATEST*`/`INITIAL_TASK*`/`HANDOFF_NEXT_SESSION*`/`handoff_next*`/`next_session*` pointers in durable locations should point to this artifact when maintained.

(End of file)
" \
filePath:
/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/.handoff/handoff_2026-11-07T09-35-58Z_INITIAL_TASK.md