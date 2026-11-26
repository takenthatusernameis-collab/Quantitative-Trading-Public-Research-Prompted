# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-26T20:10:36Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Research Phase:** Complete (E001–E043)
**Ledger:** `ledger/RESEARCH_LEDGER.md`

---

## Quick Start Commands

```bash
# Convention robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

---

## Critical Integrity Notes (Read Before Running)

1. **Golden artifacts** in `experiments/*.json` are canonical. The verification suite backs them up to `.verify_snapshot/` (gitignored, with `ACTIVE.json` pid marker), re-runs drivers, then restores. **Never leave a verification run half-finished.**

2. **Recovery if interrupted:**
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   # or
   git checkout -- experiments/
   ```

3. **Baseline protection:** `scripts/check_goldens_clean.py` (step in `scripts/check.sh`) fails if tracked artifacts differ from HEAD or stale snapshot exists. `scripts/check_golden_baseline.py` compares every tracked artifact against SHA-256 fingerprints in `ledger/golden_baseline.json`. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` — never re-pin as side effect of verification.

4. **Data cache coverage enforced** (`scripts/check_data_coverage.py`): every `data.download()` call site must have a committed parquet file matching `ledger/data_baseline.json`. E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`.

5. **Optimizer determinism (ledger E049/E050):** `src/portfolio_opt.py` validates solver answers on **problem constraints**, not solver exit status. Exact KKT active-set enumeration (commit `72dc947`) makes E041/E042 bit-reproducible. Do not re-pin to silence tolerance — no violation remains.

---

## Reproducibility Requirements

- **Seed:** Always `SEED=42` (walk-forward + placebo RNG)
- **Convention:** Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional.

---

## Current State

- Research complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All verification tiers operational (quick/extended/full)
- Golden baseline pinned in `ledger/golden_baseline.json`
- Data baseline pinned in `ledger/data_baseline.json`

---

## Next Steps (Suggested)

- Run `make check` to verify convention robustness
- Run `make verify-quick` for fast regression check
- If extending research: pre-register new experiment with falsification expectations and sensitivity grid before execution
- If modifying code: run relevant experiment drivers individually, then full verification

---

*This handoff was created automatically at session end. Update as needed for the next session.*