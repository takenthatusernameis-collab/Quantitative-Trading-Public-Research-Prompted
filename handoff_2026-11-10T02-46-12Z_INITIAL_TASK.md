# Agentic Work Session Handoff

**Timestamp:** 2026-11-10T02:47:39Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
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

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
# or
make verify
```

## Critical Baseline Integrity Notes

1. **`experiments/*.json`** are canonical research artifacts. Verification suite overwrites them during re-run and restores afterward.
2. **Never leave a verification run half-finished** — use `--restore-only` to recover if interrupted.
3. **Golden baseline** pinned in `ledger/golden_baseline.json` (SHA-256 fingerprints). Do not re-pin as side effect of verification.
4. **Data cache coverage** enforced via `scripts/check_data_coverage.py` — all `data.download()` call sites must have committed, SHA-256-pinned cache files.
5. **E029 fundamentals** pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` — fully offline-reproducible.
6. **E030 panel** committed since 2026-10-20 (ledger E048) — reproduces with 0 differences.
7. **E041 optimizer drift** root-caused (ledger E049): 133 numeric differences remain (1-ulp sensitivity of ill-conditioned QP). Do NOT re-pin to silence.

## Reproducibility Requirements

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Convention**: Close-to-close is v1.2.3 primary; overnight decomposition reported alongside
- **Offline mode**: Verification runs with `QUANT_RESEARCH_OFFLINE=1` — missing cache entries fail hard

## Open Items / Next Steps

- E041 optimizer determinism: ill-conditioned tangency QP causes 1-ulp drift (~1e-05) in min_var answers. See ledger E049.
- CI workflow template at `.github/workflow-templates/verification-gate.yml` — maintainer must create actual workflow via GitHub UI (automated agents cannot push workflows).

## Individual Experiment Drivers (for targeted runs)

```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Dependencies

```bash
pip install -r requirements.txt  # numpy, pandas, scipy, pyarrow, statsmodels, yfinance
# cvxpy/cvxopt optional; falls back to scipy.optimize
```

---

*This handoff is intended for the next agentic work session. Update as needed.*