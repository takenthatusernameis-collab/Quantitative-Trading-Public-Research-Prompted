# AGENTS.md — Project Commands & Conventions

## Project Overview

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. All experiments are pre-registered with falsification
expectations and promotion gates. **Research phase complete (E001–E043).**
Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start (reproduce / verify)

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~6 min; deterministic repro + E042 n_sim=2)
SEED=42 python3 run_all_verification.py

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow
```

## Individual Experiment Commands

```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Reproducibility

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG).
- **Convention**: Close-to-close is the v1.2.3 primary convention. Overnight
  decomposition is reported alongside for every strategy.
- **Data**: Cached parquet in `data/` (gitignored except the 2026-10-12 vintage).
  Vintage pinned in `data/vintages.json`. Cache hit is calendar-independent.
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy,
  pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` are optional; the
  portfolio optimizer falls back to `scipy.optimize` when absent.

## Project Conventions

- **Pre-registration**: Every experiment driver has a `pre_registered` JSON block
  in its output and a docstring stating gates, falsification expectations, and
  sensitivity grid before execution. Goalposts are never moved post-hoc.
- **Multiple-testing discipline**: Sensitivity grids are "reported, not gated."
  A config that clears gates in the grid requires a dedicated pre-registered
  confirmatory run with a full placebo before promotion.
- **Negative results**: Recorded honestly (REJECTED / PARTIAL) with evidence.
- **Golden files**: `experiments/*.json` are committed artifacts.
  `run_all_verification.py` backs them up before re-running and restores them
  afterward — the baseline is never modified by verification.

## CI / Automation

- The intended CI gate (`.github/workflows/verification-gate.yml`) **cannot be
  created by automated agents** — the controller (`.github/scripts/kilo-controller.sh`)
  restores and cleans `.github/workflows/` at session checkpoints, and the
  repository `GITHUB_TOKEN` lacks `workflows` push permission.
- A copyable template lives at `.github/workflow-templates/verification-gate.yml`
  with instructions in `VERIFICATION_GATE_TEMPLATE.md`. A maintainer must create
  the actual workflow via the GitHub UI.
- `make check`, `make verify`, `make verify-full` provide local equivalents.

## Lint / Format

This is a Python 3 research repository. Core scripts and experiment drivers are
checked by the verification suite (py_compile + reproducibility). There is no
separate linter configured; run `python3 -m py_compile` on changed files.
