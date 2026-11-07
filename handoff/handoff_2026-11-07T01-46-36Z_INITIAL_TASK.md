# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-07T01-46-36Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 3fb112dee77141a06634625ccd3b7e55fc794ae4 (== origin/main)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- **Working tree:** only tracked `*.pyc` bytecode drift under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/` (harmless; `git checkout -- <dir>` clears it). No source, test, experiment, ledger, or data changes.
- **Goldens:** tracked artifacts under `experiments/` match HEAD (138 tracked; `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/` returns only those 12 pyc files).
- **Baseline integrity:** `ledger/golden_baseline.json` and `ledger/data_baseline.json` are the authoritative pins. Do not re-pin as a side effect.
- **Verification snapshot:** `.verify_snapshot/` absent — no live verification run in progress.

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*
- Created this durable handoff `handoff_2026-11-07T01-45-47Z_INITIAL_TASK.md` in root, mirrored under `handoff/` and `.kilo/handoff/`, and repointed canonical handoff symlinks to this artifact.
- Did not run verification, modify experiments, change baselines, or take any research action.

## Initial Task (for next session)

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

When the next session receives an explicit user instruction to do work, it must:
1. Verify repository state (`git status`, HEAD vs origin, `.verify_snapshot/` absent, goldens clean vs HEAD/baseline pins as needed).
2. Create its own timestamped durable handoff following the established pattern (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` in root, mirrored under `handoff/` and `.kilo/handoff/`, with canonical symlinks repointed) that leaves a clear initial task message for the session after it.
3. Act only on explicit user instructions; do not invent tasks.

**Action required now:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. Do not create additional handoffs unprompted, and do not re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

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
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after interrupted run
SEED=42 python3 verify_convention_robustness.py     # convention robustness only (reads JSONs, no writes)
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff Provenance

Supersedes `handoff_2026-11-07T01-43-55Z_INITIAL_TASK.md`. This file is the authoritative initial-task message for the next session.
Durable copies: root, `handoff/`, `.kilo/handoff/`. Canonical handoff symlinks repointed to this artifact.

Handoff written by agent at 2026-11-07T01-46-36Z.
