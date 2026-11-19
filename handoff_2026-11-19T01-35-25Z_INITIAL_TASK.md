# Agentic Work Session Handoff

**Timestamp:** 2026-11-19T01:40:21Z
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

---

## Project Status

**Research Phase:** COMPLETE (E001–E043)
**Surviving Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

---

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py

# Individual experiments
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e042.py --n-sim 50
```

---

## Critical Integrity Notes (from AGENTS.md)

1. **Golden files** (`experiments/*.json`) are canonical artifacts — verification overwrites and restores them. Never leave a verification run half-finished.

2. **Recovery:** If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Baseline pinning:** `ledger/golden_baseline.json` pins SHA-256 of every artifact. Re-pinning requires explicit `python3 scripts/check_golden_baseline.py --update`

4. **Data cache coverage:** Enforced invariant — `scripts/check_data_coverage.py` validates all cache files exist, tracked, and match `ledger/data_baseline.json`

5. **Reproducibility:** Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.

---

## Open Items / Known Drift (per ledger)

- **E041:** 133 numeric differences (1-ulp QP sensitivity) — do NOT re-pin
- **E042 grid artifacts:** 29-133 differences from ill-conditioned tangency QP — do NOT re-pin
- **Optimizer determinism:** `src/portfolio_opt.py` validates on constraints, not solver status (tested in `tests/test_portfolio_opt.py`)

---

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Decide on verification scope (quick/extended/full) based on time budget
4. If running extended/full, monitor for E041/E042 drift reports in `.verify_reports/`

---

*This handoff was created automatically at session end. Update as needed.*