# Handoff - Next Agentic Work Session

**Timestamp:** 2026-11-24T16:13:37Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands
```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes
- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are canonical artifacts - verification overwrites and restores them
- **Never leave verification half-finished** - use `--restore-only` to recover if interrupted
- **Cache coverage enforced**: All data inputs must be pinned in `ledger/data_baseline.json`
- **Optimizer determinism**: Tangency QP uses exact active-set enumeration (E050 fix)

## Current State
- Research phase complete (E001–E043)
- Ledger at `ledger/RESEARCH_LEDGER.md` documents surviving strategies
- Verification suite validates 8 quick drivers + 18 extended drivers
- All 18 extended drivers reproduce with 0 differences (measured 2026-11-23T05:17Z)

## Next Steps (if any)
- Review ledger for promotion decisions on PARTIAL strategies
- Consider new pre-registered experiments beyond E043
- Monitor for data vintage updates (currently pinned at 2026-10-12/2026-10-11)