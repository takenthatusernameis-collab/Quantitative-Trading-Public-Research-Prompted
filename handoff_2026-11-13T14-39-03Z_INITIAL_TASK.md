# Agentic Work Session Handoff

**Timestamp:** 2026-11-13T15:26:50Z
**Session ID:** Initial session
**Project:** Quantitative-Trading-Public-Research-Prompted

## Session Summary

This is the initial session for the quantitative trading research project. The project contains independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data (experiments E001–E043 completed, research phase complete).

## Key Commands for Next Session

```bash
# Quick convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Project State

- **Research phase:** Complete (E001–E043)
- **Validated strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden artifacts:** `experiments/*.json` (canonical baselines)
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages)
- **Seed for reproducibility:** Always use `SEED=42`

## Important Notes

1. **Baseline integrity:** Verification suite overwrites `experiments/*.json` during run and restores after. Never leave a verification run half-finished.
2. **Recovery:** If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Do not commit verification output** - restore goldens before committing
4. **Cache coverage is enforced:** All data inputs must be pinned in `ledger/data_baseline.json`

## Next Steps for New Session

- [ ] Run `make check` to verify conventions and baseline integrity
- [ ] Run `make verify-quick` for fast verification
- [ ] Review `ledger/RESEARCH_LEDGER.md` for surviving validated strategies
- [ ] Check for any open items in the ledger (e.g., E041/E042 optimizer drift)

---

*This handoff was created automatically at session start. Update with actual work completed before ending session.*