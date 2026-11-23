# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T05:43:15Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Golden artifacts in `experiments/*.json` are canonical baselines

## Verification Commands Available
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

## Key Conventions
- **Seed**: Always use `SEED=42`
- **Data**: Cached in `data/` (gitignored except pinned vintages)
- **Golden files**: `experiments/*.json` — never modified by verification
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only`

## Next Session Starting Point
Run `SEED=42 bash scripts/check.sh` to verify environment integrity before any work.