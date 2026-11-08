# HANDOFF — Timestamped Initial Task Message
**Generated:** 2026-11-08T02:06:32Z
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main (up to date with origin/main)
**HEAD:** b631d5de chore(kilo): checkpoint agent session
**Working tree:** clean

---

## Current State

- Research phase **E001–E043 complete**. Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are the canonical golden artifacts. The verification suite (`run_all_verification.py`) backs them up to `.verify_snapshot/` (with `ACTIVE.json` pid marker) before re-running and restores afterward. **Never leave a verification run half-finished.**
- Golden baseline pinned in `ledger/golden_baseline.json`. Do **not** re-pin as a side effect of running verification — the committed golden is the authoritative record.
- Data coverage is an enforced invariant (`scripts/check_data_coverage.py`). Verification runs with `QUANT_RESEARCH_OFFLINE=1`; an unpinned input fails hard instead of silently downloading.
- **Optimizer determinism (ledger E049):** `src/portfolio_opt.py` validates a solver answer on the **problem's constraints**, never on the solver's exit status. SLSQP can report status 8 ("Positive directional derivative for linesearch") *at* a constrained optimum while returning a feasible, optimal point; gating on it made the tangency portfolio environment-dependent. The rule is pinned by `tests/test_portfolio_opt.py` (a first-class step of `scripts/check.sh`). The tangency QP itself remains ill-conditioned: a 1-ulp input perturbation moves `min_var` answers by ~1e-05, so E041/E042 grid artifacts still drift by 29–133 differences. **Do NOT re-pin them to silence that** — see the open item in the ledger.

## Known Drift / Open Items

- **E029** reproduces with 0 differences since 2026-10-20 (fundamentals snapshot pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`).
- **E030** reproduces with 0 differences since 2026-10-20 (16-ETF input panel committed and re-pinned).
- **E041** drift was root-caused on 2026-10-20 (ledger E049): it was the *optimizer's* fault, not the data, and the defect is fixed. Remaining 133 numeric differences are 1-ulp sensitivity of an ill-conditioned QP; the three structural differences are gone. Still exceeds the 1e-4 tolerance, so the extended block reports E041 as drifting. **Open item — do not re-pin.**
- Ledger open entries: **E045**, **E048**, **E049**, and the E041 open item.

## Reproduce / Verify Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh      # or: make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py      # or: make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended   # or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full       # or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py      # or: make verify

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Individual Experiment Commands

```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Conventions to Respect

- **Seed:** Always `SEED=42` (walk-forward + placebo RNG).
- **Convention:** Close-to-close is the v1.2.3 primary convention. Overnight decomposition is reported alongside for every strategy.
- **Data:** Cached parquet in `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages). Cache hit is calendar-independent.
- **Pre-registration:** Every experiment driver must have a `pre_registered` JSON block in its output and a docstring stating gates, falsification expectations, and sensitivity grid before execution. Goalposts are never moved post-hoc.
- **Multiple-testing discipline:** Sensitivity grids are "reported, not gated." A config that clears gates in the grid requires a dedicated pre-registered confirmatory run with a full placebo before promotion.
- **Negative results:** Recorded honestly (REJECTED / PARTIAL) with evidence.
- **Lint/format:** Python 3 research repo. Run `python3 -m py_compile` on changed files; the verification suite checks py_compile + reproducibility. There is no separate linter configured.

## CI / Automation Note

- The intended CI gate (`.github/workflows/verification-gate.yml`) **cannot be created by automated agents** — the controller (`.github/scripts/kilo-controller.sh`) restores and cleans `.github/workflows/` at session checkpoints, and the repository `GITHUB_TOKEN` lacks `workflows` push permission.
- A copyable template lives at `.github/workflow-templates/verification-gate.yml` with instructions in `VERIFICATION_GATE_TEMPLATE.md`. A maintainer must create the actual workflow via the GitHub UI.
- `make check`, `make verify`, `make verify-full` provide local equivalents.

## Next Session Tasks (suggested)

1. Review `ledger/RESEARCH_LEDGER.md` for open items (E045, E048, E049, E041 open item).
2. Run `SEED=42 bash scripts/check.sh` (or `make check`) for convention-robustness + template validation.
3. If extending research: new experiment drivers must include a `pre_registered` JSON block, falsification expectations, and a sensitivity grid before execution.
4. If adding a data input: commit the file and re-pin with `python3 scripts/check_data_coverage.py --update`.
5. Do **not** commit unless explicitly asked.

(End of file)
