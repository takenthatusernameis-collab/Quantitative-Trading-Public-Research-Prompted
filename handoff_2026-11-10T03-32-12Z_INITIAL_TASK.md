# Agentic Work Session Handoff

**Timestamp:** 2026-11-10T03:32:12Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main (up to date with origin/main)

## Project Status

Research phase complete (E001–E043). Surviving validated strategies are documented in
`ledger/RESEARCH_LEDGER.md`. No new research task is warranted unless explicitly assigned
by the user. Default posture: durable-handoff / housekeeping deliverables only.

## Current Working-Tree State

- Only tracked modifications are stale `__pycache__/*.pyc` files (12 files, 0 code
  changes). These are pre-existing and unrelated to any task; do not commit them.
- No verification run is in progress. No `.verify_snapshot/` active marker is present,
  so the canonical `experiments/*.json` goldens are at HEAD and intact.

## Key Verification Commands

```bash
# Fast convention-robustness + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh        # or: make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py   # or: make verify-quick

# Extended verification (~21 min; 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended   # or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full   # or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py   # or: make verify

# Recover goldens after an interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Critical Baseline Integrity Notes

1. **`experiments/*.json`** are canonical research artifacts. The verification suite
   overwrites them during re-run and restores afterward — never leave a run
   half-finished. Recovery: `--restore-only` (or `git checkout -- experiments/`).
2. **Golden baseline** pinned in `ledger/golden_baseline.json` (SHA-256). Do not
   re-pin as a side effect of verification.
3. **Golden cleanliness** enforced by `scripts/check_goldens_clean.py` and
   `scripts/check_golden_baseline.py` (run via `scripts/check.sh`). Fix mismatches
   before committing.
4. **Data cache coverage** enforced via `scripts/check_data_coverage.py`; verification
   runs with `QUANT_RESEARCH_OFFLINE=1`, so missing cache entries fail hard instead of
   silently downloading.
5. **Pinned data:** 2026-10-12 vintage in `data/vintages.json`; 2026-10-11 vintage
   committed for E026/E028/E029/E030/E034/E036/E037. E029 fundamentals in
   `data/fundamentals/` per `data/fundamentals_vintages.json`. E030 panel committed
   (ledger E048).

## Reproducibility

- **Seed:** always `SEED=42`
- **Convention:** close-to-close is v1.2.3 primary; overnight decomposition reported
  alongside for every strategy.
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow,
  statsmodels, yfinance; cvxpy/cvxopt optional — portfolio optimizer falls back to
  scipy.optimize when absent).

## Open Items / Known State

- **E041/E042 optimizer drift (ledger E049):** the tangency QP is ill-conditioned; a
  1-ulp input perturbation moves `min_var` answers by ~1e-05 (E041 ~133 numeric
  diffs, E042 grid drifts). The extended block still reports E041 as drifting. Do
  **not** re-pin it to silence that — see the open item in the ledger.
- **CI workflow:** template at `.github/workflow-templates/verification-gate.yml`;
  maintainer must create the actual workflow via GitHub UI (automated agents cannot
  push workflows; the repo `GITHUB_TOKEN` lacks `workflows` push permission).

## Useful References

- `ledger/RESEARCH_LEDGER.md` — experiment log, dispositions, and open items
- `AGENTS.md` — project commands, conventions, and enforced invariants
- `README.md` — overview and key findings
- `ledger/PRIORITIZATION.md` — experiment prioritization rationale

## Suggested Next-Session Start

1. `SEED=42 bash scripts/check.sh` to confirm baseline cleanliness and integrity.
2. Review `ledger/RESEARCH_LEDGER.md` open items before making any changes.
3. Only proceed with new work if explicitly requested by the user; preserve golden
   artifacts and pinned data/baselines. Never commit the stale `__pycache__/*.pyc`
   modifications.