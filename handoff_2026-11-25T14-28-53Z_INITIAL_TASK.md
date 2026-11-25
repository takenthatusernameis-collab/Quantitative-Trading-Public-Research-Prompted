# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T14:35:30Z
**Session ID**: Initial handoff for next agentic session
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

---

## Project Status

- **Research Phase**: Complete (experiments E001–E043 executed)
- **Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden Artifacts**: Committed in `experiments/*.json` (canonical baselines)
- **Data Vintages**:
  - 2026-10-12 vintage pinned in `data/vintages.json`
  - 2026-10-11 vintage committed (E026/E028/E029/E030/E034/E036/E037)
  - E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

---

## Key Commands (SEED=42 for reproducibility)

```bash
# Fast convention-robustness check (~seconds)
make check

# Quick verification (~8 min, 8 drivers + batch + validate + E042 n_sim=2)
make verify-quick

# Extended verification (~21 min, +18 drivers, structural match)
make verify-extended

# Full verification (~15 min, E042 n_sim=50 + 96-config sensitivity)
make verify-full

# Individual experiments
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e042.py --n-sim 50
```

---

## Critical Integrity Notes

1. **Golden files**: `experiments/*.json` are canonical. Verification overwrites then restores them — never leave a run half-finished.
2. **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Baseline pinning**: `ledger/golden_baseline.json` holds SHA-256 of committed goldens. Re-pinning requires deliberate ledger entry (see E050 precedent).
4. **Cache coverage**: Enforced invariant — `scripts/check_data_coverage.py` validates all download call sites have pinned cache files.
5. **Optimizer determinacy**: `src/portfolio_opt.py` validates on constraints, not solver exit status (ledger E049). E050 exact active-set enumeration makes E041/E042 bit-reproducible.

---

## Next Session Suggested Starting Points

- Run `make check` to verify convention robustness and baseline integrity
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and dispositions
- If extending research: pre-register new experiment with falsification expectations before execution
- If verifying: choose verification tier based on time budget (quick/extended/full)

---

## Environment

- Python 3, dependencies in `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- cvxpy/cvxopt optional (fallback to scipy.optimize)
- Offline mode: `QUANT_RESEARCH_OFFLINE=1` (used by verification suite)