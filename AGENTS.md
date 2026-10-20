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
  `d6042b0` / `9f20def`, reverted in `05b5353`, and again in `1623923`,
  reverted in `026d109`, and again in `701ed78`, reverted in `34396a9`).
  Note that `git checkout -- experiments/` restores whatever `HEAD` holds —
  if `HEAD` already carries a captured run, restore the pinned artifact
  instead (`git checkout <commit> -- experiments/<file>`, where `<commit>`
  is the last one whose SHA-256 matches `ledger/golden_baseline.json`).
- `scripts/check_golden_baseline.py` (first-class step in
  `scripts/check.sh` and step 0.5d of the suite) closes the remaining
  gap: `check_goldens_clean.py` only compares the working tree with
  HEAD, so it cannot see a *commit* that replaced the baseline. This
  guard compares every tracked artifact under `experiments/` with the
  SHA-256 fingerprint pinned in `ledger/golden_baseline.json`. Replacing
  an artifact now requires re-pinning it
  (`python3 scripts/check_golden_baseline.py --update`), which puts the
  replacement in the diff. Never re-pin as a side effect of running the
  verification suite — the ledger's standing disposition is that *the
  committed golden is the authoritative record*, not the latest re-run.

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
- **Extended drift report (reporting only)**: the `--extended` block writes
  `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` — gitignored, written
  outside `experiments/` so it can never contaminate the canonical baseline.
  Per driver/artifact it records the number of differences, how many are
  numeric vs structural, the largest relative/absolute drift and the worst
  drift as a multiple of the accepted tolerance. Deterministic (no
  timestamps/durations); it changes neither the comparison logic nor the
  tolerances. Measured 2026-10-20: 15 of the 18 extended drivers reproduce
  with 0 differences; E030 (28 numeric diffs on near-zero quantities) and E041
  (354 numeric + 3 structural) drift. **E029 is offline-reproducible since
  2026-10-20** (its yfinance fundamentals snapshot is pinned in
  `data/fundamentals/` per `data/fundamentals_vintages.json`) and reproduces
  with 0 differences; the E029 golden was deliberately re-pinned to that
  snapshot. See the ledger's E045 and E029 entries.
  **E030 also reproduces with 0 differences since 2026-10-20** (ledger E048):
  its 16-ETF input was never pinned, so every run re-downloaded it, and
  yfinance is not bit-reproducible (two consecutive downloads of the same
  request differ by up to 3.2e-06 in the resulting correlations). The panel
  is now committed and the E030 golden was deliberately re-pinned to it.
- **Convention**: Close-to-close is the v1.2.3 primary convention. Overnight
  decomposition is reported alongside for every strategy.
- **Data**: Cached parquet in `data/` (gitignored except the pinned
  **2026-10-12** and **2026-10-11** vintages). The 2026-10-12 vintage is
  pinned in `data/vintages.json`; the 2026-10-11 vintage is committed
  because E026/E028/E029/E030/E034/E036/E037 request that end date
  explicitly, which is a different cache key. Cache hit is
  calendar-independent. **E029's fundamentals are separately pinned** in
  `data/fundamentals/` per `data/fundamentals_vintages.json`; when `SEED` is
  set, `src/fundamentals.fetch_fundamentals()` reads that snapshot instead of
  the live yfinance feed, so the E029 driver is fully offline-reproducible.
- **Cache coverage is an enforced invariant** (2026-10-20, ledger E048).
  `scripts/check_data_coverage.py` resolves every `data.download()` call site
  in the drivers statically and requires that each resulting cache file
  exists, is git-tracked and matches the SHA-256 pinned in
  `ledger/data_baseline.json`. An unpinned input is a live network download,
  and yfinance is not bit-reproducible. The verification suite re-executes
  every driver with `QUANT_RESEARCH_OFFLINE=1`, so a missing cache entry
  fails hard instead of silently downloading. To add a data input, commit the
  file and re-pin with `python3 scripts/check_data_coverage.py --update`.
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
