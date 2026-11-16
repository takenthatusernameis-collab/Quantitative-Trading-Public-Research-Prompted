# Agentic Work Session Handoff

**Timestamp:** 2026-11-16T05:44:41Z
**Session:** Initial task message for next agentic work session
**Project:** Quantitative-Trading-Public-Research-Prompted

---

## Project State Summary

**Research Phase:** Complete (E001–E043)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

## Quick Commands Reference

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

## Critical Notes for Next Session

1. **Golden Files:** `experiments/*.json` are canonical research artifacts. The verification suite backs them up before re-running and restores them afterward. **Never commit verification output.**

2. **Baseline Integrity:** If `scripts/check.sh` reports a golden mismatch, fix it **before** committing. Use `SEED=42 python3 run_all_verification.py --restore-only` to recover.

3. **Data Cache:** Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant via `scripts/check_data_coverage.py`.

4. **Reproducibility:** Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.

5. **Open Items:** See `ledger/RESEARCH_LEDGER.md` for E041 optimizer determinism drift and E029/E030 pinned data status.

---

**Next Session Should:** Resume from this known-good state. Run `make check` first to verify baseline integrity before any new work.