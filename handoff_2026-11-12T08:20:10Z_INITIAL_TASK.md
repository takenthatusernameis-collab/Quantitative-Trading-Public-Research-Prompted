# Agent Handoff — 2026-11-12T08:22:06Z

## Project State
- **Repository**: Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043), surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands
```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Critical Notes
1. **Golden files**: `experiments/*.json` are canonical artifacts. Verification overwrites then restores them. Never leave a verification run half-finished.
2. **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against silent baseline replacement.
4. **Data cache**: Pinned vintages in `data/vintages.json` (2026-10-12) and `data/fundamentals_vintages.json` (E029). Cache coverage enforced by `scripts/check_data_coverage.py`.
5. **Optimizer determinism**: SLSQP status 8 is valid at constrained optimum (see `tests/test_portfolio_opt.py`, ledger E049). E041/E042 grid artifacts show 1-ulp drift — do NOT re-pin to silence.

## Current Ledger Status
- **Validated strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Open items**: E041 optimizer drift (133 numeric diffs, ill-conditioned QP), E029/E030 re-pinned to pinned data vintages

## Next Steps for Agent
1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. Choose verification tier based on time budget (quick/extended/full)
3. If interrupted, run `--restore-only` before any commits
4. Never re-pin golden artifacts without explicit ledger entry