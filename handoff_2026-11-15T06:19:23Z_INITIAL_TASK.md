# Agentic Work Session Handoff

**Timestamp:** 2026-11-15T06:19:23Z
**Session ID:** Initial handoff for next agentic work session
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status Summary

**Research Phase:** Complete (Experiments E001–E043)
**Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Verification Suite:** Operational with multiple tiers (quick/extended/full)

---

## Key Commands for Next Session

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
```

---

## Critical Integrity Notes (Read Before Running)

1. **Golden Files:** `experiments/*.json` are canonical research artifacts. The verification suite overwrites them during re-runs and restores them afterward. **Never leave a verification run half-finished.**

2. **Recovery:** If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Baseline Pinning:** `ledger/golden_baseline.json` pins SHA-256 fingerprints. Never re-pin as a side effect of verification — the committed golden is authoritative.

4. **Data Cache Coverage:** Enforced invariant (ledger E048). All `data.download()` call sites must have committed, pinned cache files. Use `scripts/check_data_coverage.py --update` to add new inputs.

5. **Optimizer Determinism:** `src/portfolio_opt.py` validates on problem constraints, not solver exit status (ledger E049). Tangency QP remains ill-conditioned; E041/E042 grid artifacts drift by 29-133 differences. **Do not re-pin to silence drift.**

---

## Known Drift (Extended Verification)

- **E030:** Now offline-reproducible (pinned 16-ETF panel, ledger E048) — 0 differences
- **E029:** Offline-reproducible (pinned fundamentals snapshot, ledger E045) — 0 differences
- **E041:** 133 numeric differences remain (1-ulp sensitivity of ill-conditioned QP, ledger E049). 3 structural differences fixed. **Do not re-pin.** Open item in ledger.

---

## Next Session Suggested Starting Points

1. Run `make check` to verify environment integrity
2. Run `make verify-quick` for fast validation
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
4. Consider addressing the E041 optimizer determinism open item

---

## Environment

- **Seed:** Always use `SEED=42` (walk-forward + placebo RNG)
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages)
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- **Optional:** `cvxpy`/`cvxopt` (falls back to `scipy.optimize`)

---

*This handoff was created automatically at session start. Update as needed during work.*
