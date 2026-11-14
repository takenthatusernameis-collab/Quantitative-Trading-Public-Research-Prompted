# Handoff - Agentic Work Session

**Timestamp:** 2026-11-14T06:38:12Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
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

## Key Notes for Next Session
- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are canonical artifacts - never commit verification output
- **Recovery**: If verification interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Data cache**: Pinned vintages in `data/` (gitignored except 2026-10-12 and 2026-10-11 vintages)
- **Offline mode**: `QUANT_RESEARCH_OFFLINE=1` enforced during verification

## Current State
- No active verification run
- Working tree clean (no uncommitted changes to experiments/)
- Ready for next task