# Agentic Work Session Handoff

**Timestamp**: 2026-11-21T22:07:25Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments are pre-registered with falsification expectations and promotion gates

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
- Verification suite backs up goldens before re-running and restores them afterward
- Never commit verification output; restore before committing if interrupted
- Data cached in `data/` (gitignored except pinned vintages)
- Cache coverage is enforced invariant (ledger E048)

## Next Steps
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
- Check `scripts/check_golden_baseline.py` for baseline integrity
- Verify data coverage with `scripts/check_data_coverage.py`