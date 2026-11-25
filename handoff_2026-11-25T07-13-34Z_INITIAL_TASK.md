# Handoff - 2026-11-25T07:13:59Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043), surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Verification Commands
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification (~8 min)
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

## Critical Notes
- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`
- **Golden baseline integrity**: `ledger/golden_baseline.json` pins SHA-256 of canonical artifacts. Never re-pin without ledger entry.
- **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`. Offline mode enforced via `QUANT_RESEARCH_OFFLINE=1`.
- **Optimizer determinacy**: E050 fix (exact KKT active-set enumeration) made E041/E042 bit-reproducible. Do not re-pin to silence tolerance.

## Last Verification Status
Run `scripts/check.sh` to confirm baseline clean before starting work.

## Next Steps (if any)
[Add specific task for next session here]