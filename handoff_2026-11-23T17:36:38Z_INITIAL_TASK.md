# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T17:40:43Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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
- Always use `SEED=42` for reproducibility
- Golden files in `experiments/*.json` are canonical artifacts
- Verification suite overwrites and restores them — never leave a run half-finished
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Data cached in `data/` (gitignored except pinned vintages)
- Dependencies: `pip install -r requirements.txt`

## Next Steps
- Resume any interrupted verification runs
- Continue research from E044 onward if needed
- Validate any new experiment drivers against pre-registered gates