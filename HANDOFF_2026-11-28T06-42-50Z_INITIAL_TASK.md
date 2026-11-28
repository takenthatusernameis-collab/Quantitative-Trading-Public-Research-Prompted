# Agentic Work Session Handoff

**Timestamp**: 2026-11-28T07:35:23Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Verification suite operational (quick/extended/full modes)

## Key Commands
```bash
# Convention robustness check (fast, offline)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min + sensitivity grid)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes
- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` — do not re-pin without ledger entry
- Data cache coverage enforced via `scripts/check_data_coverage.py`
- Seed: Always use `SEED=42` for reproducibility

## Next Steps
- Run verification suite to confirm baseline integrity
- Check `scripts/check.sh` output for any golden mismatches
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategy dispositions