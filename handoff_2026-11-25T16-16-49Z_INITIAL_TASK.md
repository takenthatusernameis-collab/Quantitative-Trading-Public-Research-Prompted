# Handoff: Initial Task for Next Agentic Session

**Timestamp:** 2026-11-25T16:16:49Z
**Session:** 2026-11-25T16:16:49Z
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

---

## Project Status

**Research Phase:** COMPLETE (E001–E043 executed)
**Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

---

## Quick Start Commands

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

## Key Artifacts (DO NOT MODIFY)

- `experiments/*.json` — Canonical research artifacts (golden files)
- `ledger/golden_baseline.json` — SHA-256 fingerprints of golden artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of data cache files
- `data/vintages.json` — Pinned data vintage (2026-10-12)
- `data/fundamentals_vintages.json` — Pinned fundamentals snapshot for E029

---

## Verification Integrity Rules

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`
2. **Never commit verification output** — restore goldens before committing
3. **Do not re-pin baselines** to silence tolerance violations — only re-pin for deliberate code changes recorded in ledger
4. **Offline mode enforced** — `QUANT_RESEARCH_OFFLINE=1` during verification; missing cache = hard fail

---

## Individual Experiment Drivers

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

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Run verification suite as needed (`verify-quick`, `verify-extended`, `verify-full`)
4. Any new experiment requires pre-registration with falsification expectations

---

**Note:** This handoff is durable and timestamped. The `handoff_CURRENT` symlink points to the latest handoff file.