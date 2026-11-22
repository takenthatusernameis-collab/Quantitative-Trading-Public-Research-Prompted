# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T04:50:01Z
**Session ID**: Initial handoff created for next agentic work session
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

---

## Project Status Summary

**Research Phase**: Complete (E001–E043)
**Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`

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

## Critical Integrity Notes

1. **Golden Files**: `experiments/*.json` are canonical artifacts — verification suite backs them up to `.verify_snapshot/` and restores after. Never leave a verification run half-finished.
2. **Baseline Pinned**: SHA-256 fingerprints in `ledger/golden_baseline.json` — do not re-pin without explicit ledger update.
3. **Data Cache**: Cached parquet in `data/` (gitignored except pinned 2026-10-12/2026-10-11 vintages). Cache coverage enforced by `scripts/check_data_coverage.py`.
4. **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.

## Open Items / Known Drift (from ledger)

- **E041**: 133 numeric differences remain (1-ulp QP sensitivity) — do not re-pin
- **E030**: Now 0 differences since 2026-10-20 (pinned 16-ETF panel)
- **E029**: Fully offline-reproducible (fundamentals pinned in `data/fundamentals/`)
- **Optimizer determinism**: Pinned by `tests/test_portfolio_opt.py` — validate on constraints, not solver status

## Next Session Initial Task

Run `SEED=42 bash scripts/check.sh` to confirm a clean, convention-robust state before any further work. If it passes, proceed with `SEED=42 python3 run_all_verification.py --skip-slow` (or full verification) and review `ledger/RESEARCH_LEDGER.md` for surviving strategies.

---

*This handoff was created automatically at session start. Update as work progresses.*
