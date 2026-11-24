# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T05:10:48Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

- **Research Phase**: Complete (E001–E043)
- **Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Current State**: Ready for verification/reproduction runs

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

## Key Integrity Notes

1. **Golden files**: `experiments/*.json` are canonical artifacts. Verification suite backs them up before re-running and restores afterward.
2. **Never commit verification output**: If interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against accidental baseline replacement
4. **Cache coverage**: Enforced invariant - all data inputs must be pinned (see `ledger/data_baseline.json`)

## Recent Context

- E050 fix (commit `72dc947`): Exact KKT active-set enumeration for tangency solver, making E041/E042 bit-reproducible
- E029 fundamentals snapshot pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` (offline-reproducible since 2026-10-20)
- E030 16-ETF panel committed (offline-reproducible since 2026-10-20)

## Next Steps (Suggested)

- Run `make verify-quick` to confirm current baseline integrity
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategy documentation
- Consider any new experiment registration or sensitivity analysis

---

*This handoff was created automatically at session start. Update as work progresses.*