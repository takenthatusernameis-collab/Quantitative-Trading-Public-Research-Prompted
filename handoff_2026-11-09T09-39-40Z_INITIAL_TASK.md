# Agentic Work Session Handoff

**Timestamp:** 2026-11-09T09:45:00Z
**Session ID:** Initial handoff for next agentic work session
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status Summary

**Research Phase:** Complete (E001–E043)
- All experiments pre-registered with falsification expectations and promotion gates
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`

**Verification Suite Status:**
- `make check` - Fast convention-robustness check + template validation (~seconds, offline)
- `make verify-quick` - Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
- `make verify-extended` - Extended verification (~21 min; quick + 18 more committed drivers, structural match)
- `make verify-full` - Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)

**Key Artifacts:**
- Canonical research artifacts: `experiments/*.json` (git-tracked goldens)
- Data cache: `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages)
- Ledger: `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`

**Reproducibility:**
- Seed: Always use `SEED=42` (walk-forward + placebo RNG)
- Data: Cached parquet in `data/`, vintages pinned in `data/vintages.json`
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

---

## Critical Conventions (Read Before Running)

1. **Golden files are sacred** - `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores them afterward. Never leave a verification run half-finished.

2. **Recovery protocol** - If interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`)

3. **Cache coverage is enforced** - `scripts/check_data_coverage.py` requires every `data.download()` call site to have a committed, SHA-256-pinned cache file. Unpinned inputs fail hard under `QUANT_RESEARCH_OFFLINE=1`.

4. **No silent re-pinning** - `scripts/check_golden_baseline.py` compares artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json`. Re-pinning requires explicit `--update` flag.

5. **Optimizer determinism** - `src/portfolio_opt.py` validates solver answers on problem constraints, not exit status. SLSQP status 8 at constrained optimum is acceptable. Tangency QP remains ill-conditioned (1-ulp perturbation moves min_var by ~1e-05).

---

## Quick Start Commands

```bash
# Fast check (convention robustness only)
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (18 more drivers)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
# or
make verify

# Skip slow batch/regression steps
SEED=42 python3 run_all_verification.py --skip-slow

# Recovery
SEED=42 python3 run_all_verification.py --restore-only
```

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

## Known Drift (Extended Verification)

| Driver | Status | Notes |
|--------|--------|-------|
| E011 | 0 diff | Reproduces exactly |
| E013 | 0 diff | Reproduces exactly |
| E015 | 0 diff | Reproduces exactly |
| E016 | 0 diff | Reproduces exactly |
| E017 | 0 diff | Reproduces exactly |
| E018 | 0 diff | Reproduces exactly |
| E019 | 0 diff | Reproduces exactly |
| E020 | 0 diff | Reproduces exactly |
| E021 | 0 diff | Reproduces exactly |
| E022 | 0 diff | Reproduces exactly |
| E025 | 0 diff | REJECTED, reproduces |
| E026 | 0 diff | Reproduces exactly |
| E028 | 0 diff | Reproduces exactly |
| E029 | 0 diff | Offline-reproducible since 2026-10-20 (fundamentals pinned) |
| E030 | 0 diff | Reproduces since 2026-10-20 (16-ETF panel committed) |
| E034 | 0 diff | Reproduces exactly |
| E036 | 0 diff | Reproduces exactly |
| E037 | 0 diff | Reproduces exactly |
| E041 | **DRIFT** | 133 numeric diffs (ill-conditioned QP), 0 structural - **Do not re-pin** |
| E042 | Lead artifact | Reproduces under some scipy builds |

**Extended drift report** written to `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored).

---

## Dependencies

```bash
pip install -r requirements.txt
# numpy, pandas, scipy, pyarrow, statsmodels, yfinance
# cvxpy/cvxopt optional (falls back to scipy.optimize)
```

---

## CI / Automation Note

The intended CI gate (`.github/workflows/verification-gate.yml`) **cannot be created by automated agents** - controller restores `.github/workflows/` at checkpoints, and `GITHUB_TOKEN` lacks `workflows` push permission. Template at `.github/workflow-templates/verification-gate.yml` with instructions in `VERIFICATION_GATE_TEMPLATE.md`. Maintainer must create via GitHub UI.

---

## Next Session Guidance

1. **Always run `make check` first** - validates conventions, goldens clean, golden baseline match, data coverage, portfolio_opt tests
2. **Never leave verification half-finished** - goldens get overwritten during run, restored after
3. **If `scripts/check.sh` reports golden mismatch, fix before committing** - checkpoint commits silently replace canonical baseline
4. **Do not re-pin E041/E042 drift** - open ledger items, ill-conditioned QP sensitivity documented
5. **Report findings in ledger** - negative results recorded honestly (REJECTED/PARTIAL) with evidence

---

**End of Handoff**