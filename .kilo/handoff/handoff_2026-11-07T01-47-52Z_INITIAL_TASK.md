# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T01-47-52Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `f3bfa5e6eb6b77459d274ed857e2f14783014df0` (== `origin/main`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- **Working tree:** only 12 tracked `*.pyc` bytecode drifts under `scripts/__pycache__/`, `src/__pycache__/`, and `tests/__pycache__/` (harmless; `git checkout -- scripts/__pycache__ src/__pycache__ tests/__pycache__` clears them). No source, test, experiment, ledger, or data changes.
- **Goldens:** no tracked diffs under `experiments/`, `data/`, or `ledger/` vs HEAD at time of handoff.
- **Baseline integrity:** `ledger/golden_baseline.json` and `ledger/data_baseline.json` are authoritative pins. Do **not** re-pin as a side effect of verification or routine work.
- **Verification snapshot:** `.verify_snapshot/` not observed as an active issue at handoff time; verify before running the suite.
- **Research phase:** complete (E001–E043). Validated strategies and decisions live in `ledger/RESEARCH_LEDGER.md`.

## Session Summary (this session)

- User requested: *“Leave a timestamped clear initial task message for the next agentic work session in a durable handoff!”*
- Created this durable handoff artifact, mirrored it, and repointed canonical handoff symlinks.
- No verification runs, no code/data/ledger/experiment changes, no baseline re-pinning.

## Initial Task for Next Session (CLEAR)

**Initial task:** Wait for explicit user instructions. When an explicit instruction arrives, act only on that instruction.

**If/when asked to do work, first verify state:**
1. `git status --short` and confirm `HEAD == origin/main` (or report divergence).
2. Confirm `.verify_snapshot/` is absent and no live verification owns it; if a stale snapshot exists, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD is known-good for goldens).
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm golden/baseline/data/optimizer guards are clean before any commit.

**Durable handoff duty:** When the next session completes a user-requested action that should be handed off, create its own timestamped handoff (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md`) in repo root, mirror to `handoff/` and `.kilo/handoff/` (and `.handoff/` if used by convention), and repoint canonical `*_LATEST*`/`INITIAL_TASK*`/`handoff_next*` symlinks to that artifact. Do not create extra handoffs unprompted.

## Do Not

- Do not re-run verification, modify `experiments/*.json` goldens, or change baselines without explicit direction.
- Do not commit verification output; if a run is interrupted, restore goldens before committing.
- Do not re-open closed items: **E049/E050** (optimizer determinism / exact KKT enumeration — artifacts reproduce with 0 diffs) and **E041/E042** ill-conditioned QP drift (closed; do not re-pin to silence residual numeric drift).
- Do not create `.github/workflows/` CI gates as an automated agent (controller/token constraints); use local `make check|verify|verify-full`.

## Reproduction Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                                   # fast guards (~seconds)
SEED=42 python3 run_all_verification.py                         # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended              # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full                  # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only          # recover goldens after interruption
SEED=42 python3 verify_convention_robustness.py                 # reads JSONs, no writes
```

## Handoff Provenance

- Supersedes: `handoff_2026-11-07T01-47-00Z_INITIAL_TASK.md` (previous `LATEST` target at handoff time).
- Durable copies: repo root, `handoff/`, `.kilo/handoff/`.
- Canonical symlinks repointed to this artifact.
