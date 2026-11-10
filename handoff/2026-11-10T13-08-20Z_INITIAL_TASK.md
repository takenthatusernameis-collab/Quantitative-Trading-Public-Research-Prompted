# Agentic Work Session Handoff

**Timestamp:** 2026-11-10T13:08:20Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project Status
- **Research Phase:** Complete (E001–E043)
- **Surviving Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Verification Suite:** Available via `run_all_verification.py` (quick/extended/full modes)
- **Prioritization:** `ledger/PRIORITIZATION.md`

## Quick Commands
```bash
# Convention robustness check (seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification (~8 min; 8 drivers in the 5a block)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 committed drivers)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Restore golden artifacts after an interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Conventions
- **Seed:** Always use `SEED=42` (walk-forward + placebo RNG)
- **Convention:** Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Golden Files:** `experiments/*.json` are canonical artifacts — never commit verification output
- **Data:** Cached parquet in `data/` (gitignored except pinned 2026-10-12/2026-10-11 vintages)
- **Cache Coverage:** Enforced invariant — `scripts/check_data_coverage.py` validates all downloads; drivers run with `QUANT_RESEARCH_OFFLINE=1`
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance); `cvxpy`/`cvxopt` optional

## Critical Notes
1. **Verification runs must never be left half-finished** — they overwrite `experiments/*.json` and restore after. Use `--restore-only` if interrupted.
2. **Do not re-pin golden baselines** to silence drift — see ledger open items (E041/E042 ill-conditioned QP, E049 optimizer determinism).
3. **CI workflow cannot be created by agents** — maintainer must create via GitHub UI from template at `.github/workflow-templates/verification-gate.yml`.
4. **`scripts/check_golden_baseline.py`** closes the gap that `check_goldens_clean.py` cannot (a committed baseline replacement). Re-pinning requires explicit `--update` and goes in the diff.

## Initial Task for Next Session
Run `make check` (convention robustness + golden baseline + template validation) to confirm repository health, then review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items before driving any further experiment work. If `make check` reports a golden mismatch, fix it before committing.

## Suggested Follow-ups
- Run `make verify-quick` for fast reproducibility of the 5a-block drivers
- Check `scripts/check_data_coverage.py` if adding any new data input (commit file + re-pin with `--update`)
- Confirm no stray verification output remains in `experiments/` after any run
