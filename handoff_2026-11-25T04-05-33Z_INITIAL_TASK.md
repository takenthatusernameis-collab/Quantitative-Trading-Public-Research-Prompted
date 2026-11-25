# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T04:05:33Z
**Session ID**: Initial handoff for next agentic work session
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project State Summary

**Research Phase**: COMPLETE (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
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

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Critical Integrity Notes

1. **Golden Files**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them during re-run and restores afterward. **Never leave a verification run half-finished**.

2. **Recovery**: If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Baseline Protection**: `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json`. Re-pinning requires deliberate action and ledger entry.

4. **Data Cache**: Cached parquet in `data/` (gitignored except pinned 2026-10-12/2026-10-11 vintages). E029 fundamentals pinned separately in `data/fundamentals/` per `data/fundamentals_vintages.json`.

5. **Offline Mode**: Verification runs with `QUANT_RESEARCH_OFFLINE=1` — missing cache entries fail hard.

## Recent Key Fixes (Ledger Entries)

- **E050**: Exact KKT active-set enumeration as primary tangency solver (commit `72dc947`) — closed E041/E042 ill-conditioned-QP drift, made artifacts bit-reproducible
- **E048**: E030 16-ETF input panel committed, golden re-pinned
- **E045**: E029 fundamentals snapshot pinned, driver fully offline-reproducible

## Individual Experiment Drivers (if needed)

```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Convention

- **Primary**: Close-to-close (v1.2.3)
- **Reported alongside**: Overnight decomposition for every strategy
- **Seed**: Always `SEED=42` (walk-forward + placebo RNG)

## Dependencies

```bash
pip install -r requirements.txt
# numpy, pandas, scipy, pyarrow, statsmodels, yfinance
# cvxpy/cvxopt optional; falls back to scipy.optimize
```

---

## Suggested Next Steps for New Session

1. Run `make check` to verify baseline integrity
2. Run `make verify-quick` for fast validation
3. Check `ledger/RESEARCH_LEDGER.md` for current disposition of all experiments
4. Review any open issues or planned follow-up experiments

---

*This handoff was created automatically at session start. Update as needed during work.*
