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

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
#   or
make verify

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover the golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Baseline Integrity (read before running the suite)

`experiments/*.json` are the canonical research artifacts. The verification
suite overwrites them while it re-runs the drivers and restores them
afterwards, so **a verification run must never be left half-finished**:

- The backup now lives in the repo-local, gitignored `.verify_snapshot/`
  with an `ACTIVE.json` marker holding the owning pid. A run that is killed
  (SIGKILL / OOM / session timeout) therefore stays recoverable.
- `scripts/check_goldens_clean.py` (first-class step in `scripts/check.sh`
  and step 0.5c of the suite) fails when a tracked artifact under
  `experiments/` differs from HEAD or when a stale snapshot is pending.
  A *live* verification run is reported, not failed.
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only`
  (or `git checkout -- experiments/`). The suite also self-recovers at
  startup and refuses to start while another live run owns the snapshot.
- If `scripts/check.sh` reports a golden mismatch, fix it **before**
  committing — a checkpoint commit that captures verification output
  silently replaces the canonical baseline (this happened in commits
  `d6042b0` / `9f20def`, reverted in `05b5353`).

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
- **Driver coverage**: `verify-quick` re-executes the 8 drivers in the 5a block
  (E012, E023, E024 --merge, E027, E035, E037, E039, E042-lead). `verify-extended`
  additionally re-executes the remaining 18 committed drivers (E011, E013, E015,
  E016, E017, E018, E019, E020, E021, E022, E025, E026, E028, E029, E030, E034,
  E036, E041) and compares each to its committed golden (excl timestamp,
  numeric_tol=1e-4). A few drivers exhibit small floating-point drift between
  runs (e.g. E011 turnover 0.06427111431948639 -> 0.06427110931499598), so the
  comparison accepts bounded numeric drift while still failing on any
  structural/string difference (missing/added keys, list length changes,
  value changes such as "8 of 96" -> "7 of 96").
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
- **Do not commit verification output**: if a run is interrupted, the working
  tree holds driver output instead of the goldens. Restore before committing
  (`run_all_verification.py --restore-only`).

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
