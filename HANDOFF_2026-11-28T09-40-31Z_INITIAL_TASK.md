# Agent Handoff — 2026-11-28T09:41:47Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Git Status**: Clean (no uncommitted changes expected)

## Key Commands for Next Session
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py

# Skip slow batch/regression steps
SEED=42 python3 run_all_verification.py --skip-slow

# Restore golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

## Individual Experiment Drivers
```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Critical Invariants (must not break)
1. **Golden files**: `experiments/*.json` are canonical artifacts. Verification backs up, re-runs, restores.
2. **Seed**: Always `SEED=42` for reproducibility.
3. **Cache coverage**: All data inputs must be pinned in `ledger/data_baseline.json` (enforced by `scripts/check_data_coverage.py`).
4. **Optimizer determinism**: Tangency QP uses exact active-set enumeration (E050 fix). Do not re-pin E041/E042.
5. **No verification output commits**: If interrupted, run `--restore-only` before committing.

## Ledger References
- E049: Optimizer determinism fix (SLSQP status-gating removed)
- E050: Exact KKT active-set enumeration for tangency solver (bit-reproducible)
- E045: E029 offline reproducibility (fundamentals pinned in `data/fundamentals/`)
- E048: E030 panel pinned (16-ETF input committed)
- E029: Fundamentals snapshot pinned per `data/fundamentals_vintages.json`

## Next Steps / Open Items
- [ ] Run `SEED=42 python3 run_all_verification.py --extended` to confirm all 26 drivers reproduce
- [ ] Verify CI gate template at `.github/workflow-templates/verification-gate.yml` is current
- [ ] Check `scripts/check_golden_baseline.py` passes against `ledger/golden_baseline.json`

## Environment
- Python 3.x with numpy, pandas, scipy, pyarrow, statsmodels, yfinance
- cvxpy/cvxopt optional (fallback to scipy.optimize)
- Data cache in `data/` (gitignored except pinned vintages 2026-10-11, 2026-10-12)