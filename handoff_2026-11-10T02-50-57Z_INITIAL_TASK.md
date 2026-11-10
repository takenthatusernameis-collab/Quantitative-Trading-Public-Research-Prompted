# Agentic Work Session Handoff

**Timestamp:** 2026-11-10T02:50:57Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. No new research task is warranted unless explicitly assigned by the user. Default to durable-handoff/housekeeping deliverables only.

## Key Verification Commands

```bash
# Fast convention-robustness + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh        # or: make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py   # or: make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended   # or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full   # or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py   # or: make verify

# Recover goldens after interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Critical Baseline Integrity Notes

1. **`experiments/*.json`** are canonical research artifacts. The verification suite overwrites them during re-run and restores afterward — never leave a run half-finished.
2. **Golden baseline** pinned in `ledger/golden_baseline.json` (SHA-256). Do not re-pin as a side effect of verification.
3. **Golden cleanliness** enforced by `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` (run via `scripts/check.sh`). Fix mismatches before committing.
4. **Data cache coverage** enforced via `scripts/check_data_coverage.py`; verification runs with `QUANT_RESEARCH_OFFLINE=1` so missing cache entries fail hard.
5. **Pinned data:** 2026-10-12 vintage in `data/vintages.json`; 2026-10-11 vintage committed for E026/E028/E029/E030/E034/E036/E037. E029 fundamentals in `data/fundamentals/` per `data/fundamentals_vintages.json`. E030 panel committed (ledger E048).

## Reproducibility

- **Seed:** always `SEED=42`
- **Convention:** close-to-close is v1.2.3 primary; overnight decomposition reported alongside
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional)

## Open Items / Known State

- **E041/E042 optimizer drift (ledger E049):** tangency QP is ill-conditioned; 1-ulp input perturbation moves min_var answers by ~1e-05 (E041 ~133 numeric diffs, E042 grid drifts). Extended block still reports drift. Do **not** re-pin to silence.
- **CI workflow:** template at `.github/workflow-templates/verification-gate.yml`; maintainer must create actual workflow via GitHub UI (agents cannot push workflows).

## Useful References

- `ledger/RESEARCH_LEDGER.md` — experiment log, dispositions, open items
- `AGENTS.md` — project commands, conventions, and invariants
- `README.md` — overview and key findings

## Suggested Next-Session Start

1. `SEED=42 bash scripts/check.sh` to confirm baseline cleanliness/integrity.
2. Review `ledger/RESEARCH_LEDGER.md` (open items) before making changes.
3. Only proceed with new work if explicitly requested; preserve golden artifacts and pinned data/baselines.
