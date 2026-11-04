# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-04T01:01:49Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `e0e6678` (matches `origin/main` exactly; clean working tree)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial Task

Research phase complete (E001–E043); surviving strategies documented in `ledger/RESEARCH_LEDGER.md`. No open task queued. Wait for explicit user instructions before any research action. Confirm repo clean and `origin/main` matches HEAD first.

## Quick Checks

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Verification Commands (if asked to reproduce)

```bash
SEED=42 python3 run_all_verification.py            # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended # (~21 min, +18 committed drivers)
SEED=42 python3 run_all_verification.py --full     # (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after an interrupted run
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.

## Handoff provenance

Supersedes `handoff_2026-11-04T01-01-05Z_INITIAL_TASK.md` (HEAD `a90ed6f`). This file is the authoritative initial-task message for the next session. Durable copies: `handoff/` and `.kilo/handoff/`.

Handoff written by agent at 2026-11-04T01:01:49Z.