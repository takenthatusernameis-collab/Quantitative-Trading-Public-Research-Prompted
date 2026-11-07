# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T12:31:06Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `4e139767` (`origin/main` in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- **Working tree:** clean at handoff creation. `git status --short --branch` reported `## main...origin/main` with no local changes; `HEAD 4e139767 == origin/main`.
  - HEAD advanced since the previous handoff (`e60d549b` → `4e139767`, both `chore(kilo): checkpoint agent session`). The intervening commit touched **only** handoff pointer symlinks and the timestamped handoff artifacts — no research code, experiments, data, or ledgers changed. Verified with `git diff --stat e60d549b 4e139767` (37 files, all under `handoff/`, `.handoff/`, `.kilo/handoff/`).
- **Verification snapshot:** `.verify_snapshot/` absent; no live verification owner detected.
  - If an interrupted run is detected later: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only with care — see AGENTS.md baseline-integrity notes).
- **Goldens / baselines:** canonical and authoritative.
  - Experiment artifacts: `experiments/*.json` pinned per `ledger/golden_baseline.json`.
  - Data inputs: pinned per `ledger/data_baseline.json`.
  - **Do not re-pin** baselines as a side effect of verification.
- **Research phase:** complete (E001–E043). Survivors/decisions documented in `ledger/RESEARCH_LEDGER.md`.
- **Closed (do not reopen):** E049/E050 (optimizer determinism / exact KKT enumeration). E041/E042 residual ill-conditioned QP numeric drift remains — **do not re-pin artifacts** to silence drift.

## Initial Task for Next Session (CLEAR)

**Wait for explicit user instructions.** Do not invent tasks, do not re-run verification "just to be sure," and do not modify experiments, baselines, pre-registered gates/grids, or outcomes without explicit direction.

**If asked to do work, verify state first:**
1. `git status --short --branch` — confirm clean state and `HEAD == origin/main` (report divergence clearly if present).
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

- **Supersedes:** `handoff_2026-11-07T12-28-03Z_INITIAL_TASK.md` (state refreshed at 2026-11-07T12:31:06Z; HEAD advanced to `4e139767`, `origin/main` in sync; intervening commit touched only handoff pointers, no research artifacts).
- **Durable copies:** repo root, `handoff/`, `.handoff/`, `.kilo/handoff/`.
- **Canonical references:** `*_LATEST*` / `INITIAL_TASK*` / `HANDOFF_NEXT_SESSION*` / `handoff_next*` / `next_session*` pointers repointed to this artifact.

(End of file)