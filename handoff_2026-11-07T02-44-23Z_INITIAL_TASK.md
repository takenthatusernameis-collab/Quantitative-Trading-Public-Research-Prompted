# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T02:44:23Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `8a0964b` (`chore(kilo): checkpoint agent session`) == `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- **Working tree:** clean (`git status --short --branch` shows `main...origin/main`, no changes).
- **Goldens:** `scripts/check_goldens_clean.py` reports `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD` (verified this session). No tracked diffs under `experiments/`, `data/`, or `ledger/`.
- **Baseline integrity:** `ledger/golden_baseline.json` and `ledger/data_baseline.json` are authoritative. Do **not** re-pin as a side effect of verification or routine work.
- **Verification snapshot:** `.verify_snapshot/` absent. No live owner; safe to run the suite only if explicitly requested.
- **Research phase:** complete (E001–E043). Validated strategies/decisions live in `ledger/RESEARCH_LEDGER.md`. Closed items (do not reopen): **E049/E050** (optimizer determinism / exact KKT enumeration, 0-diff artifacts) and **E041/E042** ill-conditioned QP drift (closed; do not re-pin to silence residual numeric drift).

## Session Summary (this session)

- User requested: “Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !”
- Confirmed repo state: `HEAD == origin/main` (`8a0964b`), clean working tree, goldens clean, no `.verify_snapshot/`.
- Reviewed prior handoff (`handoff_2026-11-07T02-43-11Z_INITIAL_TASK.md`) and observed inconsistent canonical `*_LATEST*`/`handoff_next*` symlink targets across root/handoff mirrors.
- Created this durable handoff, mirrored it to `handoff/`, `.handoff/`, and `.kilo/handoff/`, and repointed canonical symlinks to this artifact.
- No verification runs, no code/data/ledger/experiment changes, no baseline re-pinning.

## Initial Task for Next Session (CLEAR)

**Wait for explicit user instructions.** Do not invent new tasks, re-run verification “just to be sure,” modify experiments, or change baselines without explicit direction.

**If/when asked to do work, verify state first:**
1. `git status --short --branch` and confirm `HEAD == origin/main` (or report divergence).
2. Confirm `.verify_snapshot/` is absent/no live owner. If stale: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD goldens are known-good).
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing to confirm golden/baseline/data/optimizer guards.

**Durable handoff duty:** When the next session completes a user-requested action that should be handed off, create a new timestamped handoff (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md`) in repo root, mirror to `handoff/`, `.handoff/`, and `.kilo/handoff/`, and repoint canonical `*_LATEST*`/`INITIAL_TASK*`/`HANDOFF*`/`handoff_next*`/`next_session*` symlinks. Do not create extra handoffs unprompted.

## Do Not

- Do not commit verification output; if interrupted, restore goldens before committing.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a verification side effect.
- Do not re-open closed E049/E050 or E041/E042 drift items.
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

- Supersedes: `handoff_2026-11-07T02-43-11Z_INITIAL_TASK.md`.
- Durable copies: repo root, `handoff/`, `.handoff/`, `.kilo/handoff/`.
- Canonical symlinks repointed to this artifact.
