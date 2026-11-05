# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-05T03-22-00Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 6cf1ea594e7f376ef6c1f375b95e2551e7ad9328
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- **Working tree:** clean (git status empty). `__pycache__/*.pyc` are tracked bytecode artifacts; verify source is clean.
- **Goldens:** 107 tracked artifacts under `experiments/`.
- **Baseline integrity:** `ledger/golden_baseline.json` and `ledger/data_baseline.json` are the authoritative pins. Do not re-pin as a side effect.
- **Snapshot:** `.verify_snapshot/` absent (confirm no live run owns it).

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*
- Created this timestamped durable handoff following the established pattern (root + `handoff/` + `.handoff/` + `.kilo/handoff/`, repointing all `INITIAL_TASK.md` symlinks).
- Did **not** run verification, modify experiments, change baselines, or take any research action beyond creating this handoff.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must create its own timestamped durable handoff following the established pattern (`YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` in root, mirrored under `handoff/`, `.handoff/`, and `.kilo/handoff/`, repointing all root + `.handoff/` + `.kilo/handoff/` `INITIAL_TASK.md` symlinks) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed).

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Verification Commands (if explicitly asked to reproduce)

```bash
SEED=42 python3 run_all_verification.py            # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # (~21 min)
SEED=42 python3 run_all_verification.py --full     # (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs. This file is the authoritative initial-task message for the next session.
Durable copies written to: root, `handoff/`, `.handoff/`, `.kilo/handoff/`. Symlinks updated as applicable.

Handoff written by agent at 2026-11-05T03-22-00Z.
