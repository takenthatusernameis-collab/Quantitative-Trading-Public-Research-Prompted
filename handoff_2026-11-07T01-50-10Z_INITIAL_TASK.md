# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T01:50:10Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `b4375e3` (`chore(kilo): checkpoint agent session`) == `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- **Working tree:** only 12 tracked `*.pyc` bytecode drifts under `scripts/__pycache__/`, `src/__pycache__/`, and `tests/__pycache__/` (harmless). Clear with `git checkout -- scripts/__pycache__ src/__pycache__ tests/__pycache__` if desired. No source, test, experiment, ledger, or data changes.
- **Goldens:** no tracked diffs under `experiments/`, `data/`, or `ledger/` vs HEAD at handoff time.
- **Baseline integrity:** `ledger/golden_baseline.json` and `ledger/data_baseline.json` are authoritative. Do **not** re-pin as a side effect of verification or routine work.
- **Verification snapshot:** `.verify_snapshot/` not observed as active at handoff time; confirm before running the suite.
- **Research phase:** complete (E001–E043). Validated strategies/decisions live in `ledger/RESEARCH_LEDGER.md`.

## Session Summary (this session)

- User requested a durable, timestamped, clear initial task message for the next agentic work session.
- Created this handoff, mirrored it to `handoff/`, `.handoff/`, and `.kilo/handoff/`, and repointed canonical handoff symlinks.
- No verification runs, no code/data/ledger/experiment changes, no baseline re-pinning.

## Initial Task for Next Session (CLEAR)

**Wait for explicit user instructions.** When an explicit instruction arrives, act only on that instruction.

**If/when asked to do work, verify state first:**
1. `git status --short` and confirm `HEAD == origin/main` (or report divergence).
2. Confirm `.verify_snapshot/` is absent/no live owner. If stale, recover: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD goldens are known-good).
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing to confirm golden/baseline/data/optimizer guards.

**Durable handoff duty:** When the next session completes a user-requested action that should be handed off, create a new timestamped handoff (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md`) in repo root, mirror to `handoff/`, `.handoff/`, and `.kilo/handoff/`, and repoint canonical `*_LATEST*`/`INITIAL_TASK*`/`handoff_next*` symlinks. Do not create extra handoffs unprompted.

## Do Not

- Do not re-run verification, modify `experiments/*.json` goldens, or change baselines without explicit direction.
- Do not commit verification output; if interrupted, restore goldens before committing.
- Do not re-open closed items: **E049/E050** (optimizer determinism / exact KKT enumeration — 0-diff artifacts) and **E041/E042** ill-conditioned QP drift (closed; do not re-pin to silence residual numeric drift).
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

- Supersedes: `handoff_2026-11-07T01-47-52Z_INITIAL_TASK.md`.
- Durable copies: repo root, `handoff/`, `.handoff/`, `.kilo/handoff/`.
- Canonical symlinks repointed to this artifact.
