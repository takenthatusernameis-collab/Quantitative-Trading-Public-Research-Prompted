# Agentic Work Session Handoff

**Timestamp:** 2026-11-15T17:59:33Z
**Session ID:** Current working session
**Project:** Quantitative-Trading-Public-Research-Prompted

## Project Status Summary

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. Research phase is **complete**.

**Surviving validated strategies** are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Critical Baseline Integrity Rules

1. **`experiments/*.json`** are canonical research artifacts
2. Verification suite overwrites them during re-run and restores afterward
3. **Never leave a verification run half-finished** - it corrupts the baseline
4. Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
5. Golden baseline is pinned in `ledger/golden_baseline.json` - never re-pin as side effect of verification

## Data & Reproducibility

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **2026-10-12 vintage** pinned in `data/vintages.json`
- **2026-10-11 vintage** committed for E026/E028/E029/E030/E034/E036/E037
- **E029 fundamentals** pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- **Cache coverage is enforced invariant** - `scripts/check_data_coverage.py` validates all download call sites

## Known Drift Issues (Documented in Ledger)

- **E011, E030, E041** show numeric drift in extended verification (1-ulp sensitivity of ill-conditioned QP)
- **E041** has 133 numeric diffs remaining after optimizer fix (ledger E049)
- **Do NOT re-pin** drifting artifacts to silence drift - see open items in ledger

## Next Session Guidance

1. Run `make check` first to verify baseline integrity
2. If continuing verification: use appropriate `make verify-*` target
3. If modifying code: run `python3 -m py_compile` on changed files
4. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
5. All experiment drivers in `experiments/run_e*.py` with pre-registered JSON blocks

## Important Files to Reference

- `AGENTS.md` - Full project commands & conventions
- `ledger/RESEARCH_LEDGER.md` - Validated strategies & dispositions
- `ledger/golden_baseline.json` - Pinned SHA-256 fingerprints
- `ledger/data_baseline.json` - Pinned data cache fingerprints
- `scripts/check.sh` - Convention robustness check
- `run_all_verification.py` - Main verification orchestrator