# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T04-00-27Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 903a5752742bd5b53c6a4d5791c02f7be3354b83 (== origin/main)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean. No live verification run; `.verify_snapshot/` absent. No source/test/ledger change. No commit made this session.

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*
- Verified repository state against live HEAD before writing: HEAD == origin/main (`903a575`), tracked tree clean (`git status --short` empty), no uncommitted changes, `experiments/` goldens match HEAD (138 tracked), `.verify_snapshot/` absent (nothing to recover).
- Read the prior standing handoff (`handoff_2026-11-04T03-59-17Z_INITIAL_TASK.md`, HEAD `903a575` — same HEAD, so it is current, not stale) and the ledger tail (E001–E081). The prior handoff is superseded by this newer-timestamped file.
- Did **not** run verification, modify experiments, change baselines, or commit anything. No research action taken — wait for explicit user direction.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must create its own timestamped durable handoff following the established pattern (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` in the root, mirrored under `handoff/` and `.kilo/handoff/`, repointing all root + `.kilo/handoff/` symlinks) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. The baseline is clean and recoverable. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

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

Supersedes previous INITIAL_TASK handoffs (most recent prior: `handoff_2026-11-04T03-59-17Z_INITIAL_TASK.md` at HEAD `903a575`). This file is the authoritative initial-task message for the next session.
Durable copies written to: `handoff/`, root symlink targets updated.

Handoff written by agent at 2026-11-04T04:00:27Z.

(End of file)