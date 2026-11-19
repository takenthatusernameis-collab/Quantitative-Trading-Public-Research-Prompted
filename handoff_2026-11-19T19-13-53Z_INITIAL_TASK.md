# Agentic Work Session Handoff

**Timestamp:** 2026-11-19T19:16:40Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status

**Research Phase:** Complete (E001–E043)
**Surviving Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Verification Suite:** Operational with three tiers (quick/extended/full)

---

## Key Commands for Next Session

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

# Individual experiments
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

---

## Critical Integrity Notes

1. **Golden Files:** `experiments/*.json` are canonical artifacts. Verification overwrites and restores them — never leave a run half-finished.

2. **Recovery:** If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Baseline Pinning:** `ledger/golden_baseline.json` pins SHA-256 of every tracked artifact. Re-pinning requires explicit `python3 scripts/check_golden_baseline.py --update`

4. **Data Coverage:** `scripts/check_data_coverage.py` enforces all cache files exist, are git-tracked, and match `ledger/data_baseline.json`

5. **Optimizer Determinism:** `src/portfolio_opt.py` validates on constraints, not solver exit status (see ledger E049). E041/E042 grid artifacts have known 1-ulp drift — do not re-pin to silence.

---

## Reproducibility Requirements

- **Seed:** Always `SEED=42` (walk-forward + placebo RNG)
- **Convention:** Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- **Offline Mode:** Verification runs with `QUANT_RESEARCH_OFFLINE=1`

---

## Open Items (from Ledger)

- E041: 133 numeric differences remain (ill-conditioned QP, 1-ulp sensitivity) — open item, do not re-pin
- E030: Now reproduces with 0 diffs since 2026-10-20 (panel committed, golden re-pinned per E048)
- E029: Offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`)

---

## Next Session Suggested Starting Point

Run `SEED=42 bash scripts/check.sh` to verify environment integrity before any verification runs.