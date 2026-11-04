# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T03-03-54Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 9053021e15412e1becf71fd3cb7801bbb4b0b3b2
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** pycache modifications only; 0 substantive tracked changes

## Session Summary (what happened this session)

- Created a fresh timestamped initial-task handoff for the next agent session.
- No experiments modified; verification artifacts remain as committed goldens.

## Initial Task

Research phase complete (E001–E043); surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. The baseline is clean and recoverable.

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
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents (see AGENTS.md). Use local `make check/verify/*`.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs. This file is the authoritative initial-task message for the next session.
Durable copies written to: `handoff/`, root symlink targets updated.

Handoff written by agent at 2026-11-04T03-03-54Z.
