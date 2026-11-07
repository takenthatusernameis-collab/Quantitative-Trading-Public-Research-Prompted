# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T04:53:54Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `b50df67` (`chore(kilo): checkpoint agent session`) == `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- **Working tree:** clean at handoff creation (no uncommitted tracked changes; no `.verify_snapshot/`).
- **HEAD vs origin:** in sync (`b50df67` == `origin/main`).
- **Goldens:** canonical baseline unchanged; no re-pinning. Tracked `experiments/*.json` (107 files) remain authoritative (`ledger/golden_baseline.json`).
- **Research phase:** complete (E001–E043). Survivors documented in `ledger/RESEARCH_LEDGER.md`.
- **Closed (do not reopen):** E049/E050 (optimizer determinism / exact KKT enumeration); E041/E042 ill-conditioned QP residual drift — do **not** re-pin to silence numeric drift.

## Session Summary (this session)

- User requested a timestamped, clear initial-task message for the next agentic session in a durable handoff.
- Verified state: `b50df67` == `origin/main`, clean tree, `.verify_snapshot/` absent, durable handoff dirs present (`handoff/`, `.handoff/`, `.kilo/handoff/`).
- Reviewed prior handoff `handoff_2026-11-07T04-52-51Z_INITIAL_TASK.md`; state unchanged except this refresh.
- No verification runs, no experiment/code/ledger/golden/data-baseline changes.
- Created this durable handoff, mirrored it to durable locations, and repointed canonical latest/initial-task/next-session symlinks.

## Initial Task for Next Session (CLEAR)

**Wait for explicit user instructions.** Do not invent tasks, do not re-run verification "just to be sure," and do not modify experiments/baselines without explicit direction.

**If asked to do work, verify first:**
1. `git status --short --branch` — confirm `HEAD == origin/main` (or report divergence).
2. Confirm `.verify_snapshot/` absent/no live owner. If stale: `SEED=42 python3 run_all_verification.py --restore-only`.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing.

**Durable handoff duty:** When completing a user-requested action that needs handoff, create a new timestamped `handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md`, mirror to `handoff/`, `.handoff/`, `.kilo/handoff/`, and repoint canonical `*_LATEST*`/`INITIAL_TASK*`/`HANDOFF_NEXT_SESSION*`/`handoff_next*`/`next_session*` symlinks. Do not create extra handoffs unprompted.

## Do Not

- Do not commit verification output; restore goldens before committing if interrupted.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect of verification.
- Do not re-open closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent; use local `make check|verify|verify-full`.
- Do not change pre-registered gates/sensitivity grids/outcomes without explicit justification and ledger update.

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

- Supersedes: `handoff_2026-11-07T04-52-51Z_INITIAL_TASK.md` (refresh; state unchanged).
- Durable copies: repo root, `handoff/`, `.handoff/`, `.kilo/handoff/`.
- Canonical symlinks repointed to this artifact.

(End of file - total 58 lines)