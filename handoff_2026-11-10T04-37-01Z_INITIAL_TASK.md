# HANDOFF — Next Agentic Work Session
**Timestamp**: 2026-11-10T04:44:55Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Git Branch**: main (up to date with origin/main)
**Project State**: Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md` and `experiments/FINAL_SUMMARY.json`.

---

## Project Overview
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates.

**Key Artifacts**:
- `ledger/RESEARCH_LEDGER.md` — Full experiment log (E001–E043)
- `experiments/FINAL_SUMMARY.json` — Canonical summary of surviving/rejected strategies
- `experiments/validation_summary.json` — Baseline E001 factor sweep results
- `ledger/golden_baseline.json` — SHA-256 fingerprints of 107 committed experiment JSONs
- `data/vintages.json` + `data/fundamentals_vintages.json` — Pinned data cache keys

---

## Surviving Validated Strategies (from FINAL_SUMMARY.json)

| Experiment | Strategy | Universe | OOS Sharpe (c2c) | Status |
|------------|----------|----------|------------------|--------|
| E010/E015 | TSM Pure (Equity Flagship) | large_liquid (130) | 1.724 | **VALIDATED** — equity flagship (β-bearing) |
| E012/E013 | Dollar-Neutral Low-Beta Sort | large_liquid (130) | 1.053 | **VALIDATED** — equity market-neutral (β ≈ -0.035) |
| E018 | Futures TSM 18m | 16-contract de-seamed futures | 0.841 | **VALIDATED** — cross-asset trend |
| E017 | Futures Carry (Realized Roll Yield) | 16-contract futures | 0.472 | **NEAR-SIGNIFICANT** — diversifier candidate |
| E022 | Macro Momentum (Brooks 2017) | SPY/IEF/GLD | 0.006 c2c / 0.428 overnight | **REJECTED standalone** — retained as crisis-alpha diversifier |

**Key Finding**: No promoted strategy survives v1.2.3 convention-aligned gates as a **market-neutral total portfolio**. The only surviving market-neutral strategy is DN low-beta (E012/E013); all others carry equity beta or fail gates.

---

## Rejected / Data-Infeasible (Notable)
- **E021** Pairs Trading (distance): OOS Sharpe 0.315, placebo z=0.77 → REJECTED
- **E025** Cointegration Stat-Arb: OOS Sharpe -0.573, placebo z=-0.86 → REJECTED
- **E029, E031, E032, E033** Fundamental factors (Profitability, Accruals, PEAD, QMJ): **DATA-INFEASIBLE** — yfinance quarterly APIs return only ~6 trailing quarters vs ~50 required
- **E030** Multi-Asset TSM (ETFs): Beta 0.532, bear Sharpe -1.421 → REJECTED
- **E035** Liquidity (Amihud): Convention-fragile, parameter-fragile → REJECTED
- **E037** Portfolio Integration (Low-Vol + Vol-Scaling): Beta 0.512, bear Sharpe -1.79 → REJECTED
- **E039** Extended Macro-Momentum: Themes collinear, degrade edge → REJECTED

---

## Verification Suite (run before any changes)

```bash
# Fast convention-robustness + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 drivers + batch_run + validate + E042 n_sim=2)
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

# Recover golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

**Critical**: The verification suite overwrites `experiments/*.json` while running and restores them afterward. **Never leave a verification run half-finished**. If interrupted, run `--restore-only` or `git checkout -- experiments/` before committing.

---

## Reproducibility Invariants
- **Seed**: Always `SEED=42` (walk-forward + placebo RNG)
- **Convention**: v1.2.3 — close-to-close is primary; overnight decomposition reported alongside
- **Data**: Cached parquet in `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages). E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- **Cache Coverage**: Enforced invariant (ledger E048). `scripts/check_data_coverage.py` requires every `data.download()` call site to have a committed, SHA-256-pinned cache file. Unpinned input = live network download = non-reproducible.
- **Offline Execution**: Verification runs with `QUANT_RESEARCH_OFFLINE=1`; missing cache entries fail hard.

---

## Open Items / Next High-Value Work (from Ledger)

1. **Market-Neutral Total Portfolio** — No strategy survives as market-neutral total portfolio. The DN low-beta (E012/E013) is the only market-neutral equity strategy. Consider:
   - Blending TSM Pure (β=0.90) with DN low-beta (β≈0) + futures TSM/carry for cross-asset diversification
   - Volatility targeting / risk parity across the validated legs

2. **Equity Universe Expansion** — Current validated equity strategies use `large_liquid` (130 tickers). The original E001 sweep used only 10 sector ETFs. Re-validating on a broader universe (top ~500 US large-caps) is the cheapest high-information experiment.

3. **E041 Optimizer Drift** — Ill-conditioned QP in `src/portfolio_opt.py` causes 1-ulp sensitivity (133 numeric diffs in extended verification). **Do not re-pin to silence** — see ledger E049 open item. The solver validation rule (feasibility on constraints, not exit status) is pinned by `tests/test_portfolio_opt.py`.

4. **E030/E041 Drift Reports** — Extended verification reports drift for E030 (28 numeric diffs on near-zero quantities) and E041 (133 numeric diffs). Both are within expected numerical tolerance for ill-conditioned problems.

5. **CI Gate** — `.github/workflows/verification-gate.yml` cannot be created by automated agents. Template at `.github/workflow-templates/verification-gate.yml` with instructions in `VERIFICATION_GATE_TEMPLATE.md`. A maintainer must create via GitHub UI.

---

## Current Working Tree Status
- Only `__pycache__/*.pyc` files modified (no source changes)
- All golden artifacts match `ledger/golden_baseline.json` fingerprints
- No pending verification run (snapshot clean)

---

## Quick Start for Next Session
```bash
cd /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
SEED=42 bash scripts/check.sh   # Verify baseline integrity first
# Then explore:
# - ledger/RESEARCH_LEDGER.md for full experiment details
# - src/batch_run.py, src/validate.py for pipeline entry points
# - experiments/run_e042.py for min-var confirmatory (PARTIAL)
# - experiments/run_e041.py for market-neutral portfolio (REJECTED)
```

---

**End of Handoff** — This document is durable and should be read at the start of the next agentic work session.