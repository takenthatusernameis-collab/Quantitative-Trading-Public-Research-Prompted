# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T17:40:52Z
**Session**: Initial task message for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Artifacts
- **Golden files**: `experiments/*.json` (committed artifacts, never modified by verification)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (surviving validated strategies)
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Baseline integrity**: `ledger/golden_baseline.json` (SHA-256 fingerprints)

## Important Notes
- Always use `SEED=42` for reproducibility
- Verification suite backs up golden files before re-running and restores them afterward
- Never commit verification output; restore before committing (`--restore-only`)
- Cache coverage is enforced: all data inputs must be pinned in `ledger/data_baseline.json`
- Optimizer determinism issue tracked in ledger E049 (E041/E042 grid artifacts drift)

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Use `make verify-quick` for fast validation
4. Review any open items in the ledger (E041 drift, E049 optimizer determinism)