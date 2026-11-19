# Agentic Work Session Handoff

**Timestamp**: 2026-11-19T18:16:21Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Verification suite operational: `make check`, `make verify`, `make verify-full`

## Key Commands
```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

## Important Notes
- Golden files in `experiments/*.json` are canonical artifacts
- Verification overwrites and restores them — never leave a run half-finished
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Data cached in `data/` (gitignored except pinned vintages)
- Cache coverage enforced by `scripts/check_data_coverage.py`
- SEED=42 required for reproducibility

## Next Steps
- Run verification suite to confirm baseline integrity
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
- Check `scripts/check.sh` passes before committing