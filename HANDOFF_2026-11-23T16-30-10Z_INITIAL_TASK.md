# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T16:31:39Z
**Session ID**: Initial handoff for next agentic session
**Project**: Quantitative-Trading-Public-Research-Prompted

---

## Project State Summary

**Research Phase**: Complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates

**Verification Status**:
- `verify-quick` (8 min): 8 experiment drivers re-executed + batch_run + validate + E042 n_sim=2
- `verify-extended` (21 min): + 18 more committed drivers, structural match with numeric_tol=1e-4
- `verify-full` (15 min): E042 n_sim=50 + 96-config sensitivity grid

**Key Baselines**:
- Golden artifacts in `experiments/*.json` (canonical research artifacts)
- Pinned SHA-256 fingerprints in `ledger/golden_baseline.json`
- Data vintages: 2026-10-12 (pinned in `data/vintages.json`) and 2026-10-11 (committed)
- E029 fundamentals separately pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

**Critical Invariants**:
1. **Baseline integrity**: Verification suite overwrites `experiments/*.json` during runs and restores them afterward — never leave a run half-finished
2. **Cache coverage**: Enforced by `scripts/check_data_coverage.py` — every `data.download()` call must have a committed, SHA-256-pinned cache file
3. **Convention**: Close-to-close is v1.2.3 primary; overnight decomposition reported alongside
4. **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
5. **Optimizer determinism**: `src/portfolio_opt.py` validates on problem constraints, not solver exit status (ledger E049/E050)

---

## Quick Start Commands

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

# Full verification (~15 min)
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

---

## Individual Experiment Commands

```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

---

## Recent Key Findings (from Ledger)

- **E049** (2026-10-20): Optimizer determinism root-caused — SLSQP status 8 is scipy-build dependent; gating on it made tangency portfolio environment dependent. Fixed by validating on constraints, not exit status.
- **E050** (2026-11-01): Exact KKT active-set enumeration as primary tangency solver — made E041/E042 artifacts bit-reproducible across environments (0 differences at 2026-11-23 measurement).
- **E029**: Offline-reproducible since 2026-10-20 (fundamentals snapshot pinned)
- **E030**: Reproduces with 0 differences since 2026-10-20 (16-ETF panel committed)
- **E041**: Drift root-caused to optimizer, not data — fixed by E050 exact solver

**Do NOT re-pin E041/E042 artifacts** to silence tolerance violations — there are none remaining. Re-pinning only warranted for deliberate code changes recorded in ledger first.

---

## Next Session Guidance

1. **Always run `make check` first** — verifies golden baseline integrity, convention robustness, data coverage, and optimizer determinism tests
2. **Never leave verification half-finished** — use `--restore-only` if interrupted
3. **Check `ledger/RESEARCH_LEDGER.md`** for surviving strategies and disposition history
4. **All drivers are pre-registered** — check docstrings for gates, falsification expectations, sensitivity grids
5. **CI workflow cannot be created by agents** — template at `.github/workflow-templates/verification-gate.yml`

---

## Dependencies

```bash
pip install -r requirements.txt
# numpy, pandas, scipy, pyarrow, statsmodels, yfinance
# cvxpy/cvxopt optional (falls back to scipy.optimize)
```

---

*This handoff was created automatically at session start. Update as needed for subsequent sessions.*