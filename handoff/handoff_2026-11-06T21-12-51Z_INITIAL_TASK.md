# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-06T21-12-51Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 17ab5037eb4ba54c54b241b60a27fc9cc154bada (== origin/main)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- **Working tree:** 12 modified `*.pyc` files under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/`. These are tracked in git (not gitignored) and were modified by prior sessions' Python runs; they are **bytecode artifacts, not source**. No source, test, experiment, or ledger changes. `git diff --name-only HEAD -- experiments/` is empty.
- **`.verify_snapshot/` absent** — no live verification run is in progress.
- **Baseline integrity:** `ledger/golden_baseline.json` and `ledger/data_baseline.json` are the authoritative pins. Do not re-pin as a side effect.

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !*
- Verified state before writing: HEAD == origin/main (`17ab503`), `.verify_snapshot/` absent, goldens match HEAD, only `__pycache__/*.pyc` dirty, no untracked files.
- Did **not** run verification, modify experiments, change baselines, or take any research action. No explicit user direction beyond the handoff request.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must create its own timestamped durable handoff following the established pattern (`YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` under `handoff/`, repointing root symlinks `INITIAL_TASK.md`, `handoff.md`, `next_session.md`, `handoff_next.md`, `handoff_next_session.md`, and `handoff_LATEST*/LATEST*` aliases) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed).

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Verification Commands (if explicitly asked to reproduce)

```bash
SEED=42 python3 run_all_verification.py            # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended # (~21 min, +18 committed drivers)
SEED=42 python3 run_all_verification.py --full     # (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after an interrupted run
SEED=42 python3 verify_convention_robustness.py     # convention robustness only (reads JSONs, no writes)
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs (most recent prior: 2026-11-06T21-11-38Z_INITIAL_TASK.md). This file is the authoritative initial-task message for the next session. Durable copy written under `handoff/`; root symlinks updated to point here.

Handoff written by agent at 2026-11-06T21-12-51Z.
" \
  /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/handoff/handoff_2026-11-06T21-12-51Z_INITIAL_TASK.md