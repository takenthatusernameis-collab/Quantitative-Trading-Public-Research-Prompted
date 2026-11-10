# Agentic Work Session Handoff

**Timestamp:** 2026-11-10T13:09:25Z
**Session ID:** Initial handoff for next agentic session
**Project:** Quantitative-Trading-Public-Research-Prompted

---

## Project Status Summary

**Research Phase:** COMPLETE (Experiments E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates

**Verification Suite Status:**
- `verify-quick` (~8 min): 8 core drivers (E012, E023, E024, E027, E035, E037, E039, E042-lead)
- `verify-extended` (~21 min): +18 committed drivers with structural match
- `verify-full` (~15 min): E042 n_sim=50 + 96-config sensitivity grid

**Key Artifacts:**
- Golden baselines: `experiments/*.json` (canonical, committed)
- Data vintages: `data/vintages.json` (2026-10-12 pinned), `data/fundamentals_vintages.json` (E029 fundamentals)
- Ledger: `ledger/golden_baseline.json` (SHA-256 fingerprints), `ledger/data_baseline.json`

---

## Critical Conventions (MUST FOLLOW)

1. **Never leave verification half-finished** — run restores goldens on completion; interrupted runs leave driver output in `experiments/`
2. **Seed always `SEED=42`** for walk-forward + placebo RNG
3. **Offline mode enforced** — `QUANT_RESEARCH_OFFLINE=1` during verification; missing cache = hard failure
4. **Golden integrity** — `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against silent baseline replacement
5. **Do not re-pin to silence drift** — E041/E042 optimizer drift is known (ill-conditioned QP), documented in ledger E049

---

## Quick Commands

```bash
# Convention robustness only (fast, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification (8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Recover goldens after interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

---

## Known Issues / Open Items

1. **E041 drift** — 133 numeric differences (1-ulp sensitivity of ill-conditioned QP), 3 structural diffs resolved. Do NOT re-pin. See ledger E049.
2. **E042 grid artifacts** — 29-133 differences from same optimizer sensitivity. Do NOT re-pin.
3. **CI gate** — `.github/workflows/verification-gate.yml` cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml`
4. **Cache coverage** — enforced invariant; `scripts/check_data_coverage.py --update` to add new inputs

---

## Next Session Suggested Starting Points

- Run `SEED=42 bash scripts/check.sh` to verify environment integrity
- Check `ledger/RESEARCH_LEDGER.md` for latest dispositions
- If continuing verification: decide on `verify-quick` vs `verify-extended` vs `verify-full`
- If adding experiments: follow pre-registration template in existing drivers

---

## Environment

- Python 3, dependencies: `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- Optional: cvxpy/cvxopt (fallback to scipy.optimize)
- Data cache in `data/` (gitignored except pinned vintages)

---

*This handoff is durable — commit or copy to persist across sessions.*