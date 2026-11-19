# Agentic Work Session Handoff

**Timestamp**: 2026-11-19T20:08:15Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Session Context

This is a quantitative research repository for US equities, futures, and macro data (2014–2026). Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

```bash
# Fast convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes

- **Never leave verification half-finished**: The suite backs up `experiments/*.json` to `.verify_snapshot/` and restores after. If killed, recover with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Golden baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against accidental baseline replacement
- **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`. Cache coverage enforced by `scripts/check_data_coverage.py`
- **Reproducibility**: Always use `SEED=42`. Convention is close-to-close v1.2.3 primary with overnight decomposition reported alongside

## Current State

- Research phase complete (E001–E043)
- Ledger at `ledger/RESEARCH_LEDGER.md` documents surviving strategies
- Verification suite ready to run
- No active experiment runs in progress

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment health
2. Choose verification level: `verify-quick`, `verify-extended`, or `verify-full`
3. Review `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
4. Any new experiments require pre-registration with falsification expectations

---
*Generated automatically for session handoff*