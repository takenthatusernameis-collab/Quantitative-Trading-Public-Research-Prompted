# Agentic Work Session Handoff

**Timestamp**: 2026-11-17T07:17:15Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Notes
- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are canonical artifacts - never commit verification output
- **Recovery**: If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only`
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Dependencies**: `pip install -r requirements.txt`

## Verification Integrity
- Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker
- `scripts/check_goldens_clean.py` compares working tree with HEAD
- `scripts/check_golden_baseline.py` compares with SHA-256 in `ledger/golden_baseline.json`
- Never re-pin artifacts as side effect of verification

## Next Steps
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
- Run verification suite to confirm baseline integrity
- Check for any open items in ledger (E049 optimizer determinism, E041 drift)