# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T04:10:48Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. Research phase is complete. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

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

1. **Golden files**: `experiments/*.json` are canonical research artifacts. The verification suite overwrites them during re-runs and restores them afterward. **Never leave a verification run half-finished** - it must complete or be restored with `SEED=42 python3 run_all_verification.py --restore-only`

2. **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` (both in `scripts/check.sh`) guard against accidental baseline replacement. If `scripts/check.sh` reports a golden mismatch, fix it **before** committing.

3. **Cache coverage**: `scripts/check_data_coverage.py` enforces that every data download call site has a pinned cache file. All drivers re-execute with `QUANT_RESEARCH_OFFLINE=1`, so missing cache entries fail hard.

4. **Reproducibility**: Always use `SEED=42`. The 2026-10-12 vintage is pinned in `data/vintages.json`; the 2026-10-11 vintage is committed for experiments that explicitly request that end date. E029 fundamentals are separately pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`.

5. **Optimizer determinacy**: `src/portfolio_opt.py` validates solver answers on problem constraints, not solver exit status. The E050 fix (exact KKT active-set enumeration) made E041/E042 artifacts bit-reproducible. Do **not** re-pin to silence tolerance violations.

## Current State

- Research phase: **Complete** (E001–E043)
- Verification suite: Available and tested
- Golden baseline: Pinned in `ledger/golden_baseline.json`
- Data baseline: Pinned in `ledger/data_baseline.json`
- No active verification run in progress

## Suggested Next Steps

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Run `SEED=42 python3 run_all_verification.py` for quick verification
3. Check `ledger/RESEARCH_LEDGER.md` for surviving validated strategies
4. Review any open issues in the ledger for follow-up experiments

---

*This handoff was created automatically at session start. Update as needed during work.*