# HANDOFF - 2026-11-04T03:06:42Z

## Current State
- **Research phase complete**: E001–E043 finished. Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Verification suite active**: Guards in place (`scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`). Never leave a verification run half-finished.
- **Optimizer determinism**: Fixed (E049) - solver exit status no longer gates on SLSQP status 8. `tests/test_portfolio_opt.py` enforces validation against constraints.
- **Open issue**: E041 still drifts in extended verification (133 numeric differences, 1-ulp sensitivity from ill-conditioned QP). Structural diffs resolved. Do **not** re-pin to silence this.

## Initial Task for Next Session (Priority 1)
**Investigate and address E041 numerical drift.**

Steps:
1. Read `ledger/RESEARCH_LEDGER.md` (E041, E049) and `src/portfolio_opt.py` to understand the ill-conditioned tangency QP.
2. Review `tests/test_portfolio_opt.py` for determinism constraints.
3. Run extended verification to confirm current state: `SEED=42 python3 run_all_verification.py --extended`
4. Determine if drift can be reduced (better conditioning/numerics) or if tolerance/acceptance needs to be codified without re-pinning goldens.
5. Update ledger with findings before committing any changes.

## Quick Commands
```bash
# Fast checks
SEED=42 bash scripts/check.sh

# Quick verification (8 drivers)
SEED=42 python3 run_all_verification.py --quick

# Extended (includes E041)
SEED=42 python3 run_all_verification.py --extended

# Recover if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

## Critical Rules
- Always use `SEED=42`
- Never modify `experiments/*.json` goldens without re-pinning via `scripts/check_golden_baseline.py --update`
- Run with `QUANT_RESEARCH_OFFLINE=1` behavior enforced by suite; missing caches fail hard
- If `check_goldens_clean.py` reports mismatch, restore from HEAD or pinned commit first
