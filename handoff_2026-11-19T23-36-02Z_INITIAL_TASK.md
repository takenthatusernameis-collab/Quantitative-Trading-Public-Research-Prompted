# Handoff: Next Agentic Work Session
**Timestamp:** 2026-11-19T23:36:02Z
**Session Type:** Initial Task Message
**Project:** Quantitative-Trading-Public-Research-Prompted

---

## Project State Summary

**Research Phase:** Complete (E001–E043)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Current Verification Baseline:** `experiments/*.json` (canonical artifacts, git-tracked)

---

## Key Verification Commands

| Command | Duration | Purpose |
|---------|----------|---------|
| `SEED=42 bash scripts/check.sh` | ~seconds | Fast convention-robustness + template validation (offline) |
| `SEED=42 python3 run_all_verification.py` | ~8 min | Quick full verification (8 drivers + batch_run + validate + E042 n_sim=2) |
| `SEED=42 python3 run_all_verification.py --extended` | ~21 min | Extended (quick + 18 more drivers, structural match) |
| `SEED=42 python3 run_all_verification.py --full` | ~15 min | Full (E042 n_sim=50 + 96-config sensitivity grid) |
| `SEED=42 python3 verify_convention_robustness.py` | ~seconds | Convention robustness only (reads JSONs, no writes) |

---

## Critical Integrity Rules (from AGENTS.md)

1. **Golden files (`experiments/*.json`)** are canonical artifacts. Verification suite backs them up before re-running and restores after. **Never commit verification output.**
2. **If `scripts/check.sh` reports a golden mismatch, fix it BEFORE committing** — checkpoint commits silently replace canonical baseline.
3. **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
4. **Cache coverage is enforced** — `scripts/check_data_coverage.py` validates every `data.download()` call site resolves to committed, SHA-256-pinned parquet.
5. **Offline execution:** Verification runs with `QUANT_RESEARCH_OFFLINE=1` — missing cache = hard fail.

---

## Current Open Items (from Ledger)

- **E041/E042 optimizer drift:** 1-ulp sensitivity of ill-conditioned QP (SLSQP status 8 handling fixed, but `min_var` answers still drift ~1e-05). **Do not re-pin to silence.**
- **E030 drift resolved** (2026-10-20, ledger E048): 16-ETF panel now committed, golden re-pinned.
- **E029 offline-reproducible** (2026-10-20, ledger E045): fundamentals pinned in `data/fundamentals/`.
- **E049:** Optimizer determinism rule pinned by `tests/test_portfolio_opt.py` (validates on problem constraints, not solver exit status).

---

## Reproducibility Requirements

- **Seed:** Always `SEED=42` (walk-forward + placebo RNG)
- **Convention:** Close-to-close primary (v1.2.3); overnight decomposition reported alongside
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages 2026-10-11/2026-10-12)
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance); cvxpy/cvxopt optional

---

## Next Session Suggested Starting Points

1. **Run quick verification:** `SEED=42 python3 run_all_verification.py` to confirm baseline integrity
2. **Check goldens clean:** `SEED=42 bash scripts/check.sh` (includes `check_goldens_clean.py` + `check_golden_baseline.py`)
3. **Review ledger:** `cat ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
4. **Extended verification if time permits:** `SEED=42 python3 run_all_verification.py --extended`

---

## Workspace Notes

- `handoff_CURRENT`, `handoff_LATEST`, `handoff_NEXT` symlinks all point to latest handoff
- `.verify_snapshot/` (gitignored) holds backup during verification runs with `ACTIVE.json` marker
- `.verify_reports/` (gitignored) holds extended drift reports
- No CI workflow committed (template at `.github/workflow-templates/verification-gate.yml`)

---

*This handoff created automatically for session continuity. Next agent should verify baseline before making changes.*