# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T01:23:02Z
**Session**: Initial handoff for next agentic work session
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

---

## Project State Summary

**Research Phase**: Complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates
- Golden artifacts in `experiments/*.json` are canonical baselines

---

## Verification Commands (Ready to Run)

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

---

## Critical Integrity Notes (Read Before Running)

1. **Golden artifacts are protected**: `experiments/*.json` are backed up to `.verify_snapshot/` during verification and restored afterward. Never leave a verification run half-finished.

2. **Baseline integrity checks** (run automatically in `scripts/check.sh`):
   - `check_goldens_clean.py`: Fails if tracked artifacts differ from HEAD or stale snapshot exists
   - `check_golden_baseline.py`: Compares every artifact with SHA-256 in `ledger/golden_baseline.json`
   - `check_data_coverage.py`: Enforces all data inputs are pinned (cache hit is calendar-independent)

3. **Recovery if interrupted**:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   # or
   git checkout -- experiments/
   ```

4. **Key recent fixes (ledger entries)**:
   - E050: Exact KKT active-set enumeration for tangency solver → bit-reproducible artifacts
   - E049: Optimizer determinism - validate on constraints, not solver exit status
   - E048: Cache coverage enforced - all data inputs pinned
   - E045/E029: E029 fundamentals snapshot pinned for offline reproducibility
   - E030: 16-ETF panel committed for reproducibility

---

## Individual Experiment Drivers (Committed)

```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

---

## Dependencies

```bash
pip install -r requirements.txt
# numpy, pandas, scipy, pyarrow, statsmodels, yfinance
# cvxpy/cvxopt optional (falls back to scipy.optimize)
```

---

## Convention & Data

- **Primary convention**: Close-to-close (v1.2.3), overnight decomposition reported alongside
- **Data cache**: `data/` (parquet, gitignored except pinned 2026-10-12 / 2026-10-11 vintages)
- **E029 fundamentals**: Separately pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- **Reproducibility seed**: Always `SEED=42` (walk-forward + placebo RNG)

---

## Next Steps for New Session

1. Run `make check` to verify environment and baseline integrity
2. Run `make verify-quick` for fast verification (~8 min)
3. If quick passes, consider `make verify-extended` for full driver coverage
4. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and dispositions
5. All experiments are pre-registered — do not move goalposts post-hoc

---

**Status**: Ready for verification / continuation. No blockers.