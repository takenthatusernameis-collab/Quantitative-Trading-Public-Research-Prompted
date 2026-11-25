# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T14:28:13Z
**Session ID**: Initial session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Current State

- Research phase complete (E001–E043)
- All experiments have pre-registered falsification expectations and promotion gates
- Golden files in `experiments/*.json` are canonical research artifacts
- Verification suite overwrites them during runs and restores afterward
- Data cached in `data/` (gitignored except pinned vintages)
- SEED=42 for reproducibility

## Next Session Priorities

1. **Review ledger/RESEARCH_LEDGER.md** for surviving validated strategies
2. **Run verification** to confirm baseline integrity: `SEED=42 make verify-quick`
3. **Check for any interrupted verification runs** that need recovery: `SEED=42 python3 run_all_verification.py --restore-only`
4. **Review open issues** in the research ledger for potential follow-up experiments

## Important Notes

- **Never leave verification half-finished** - it overwrites golden files and must restore them
- If `scripts/check.sh` reports golden mismatch, fix before committing
- `git checkout -- experiments/` restores HEAD; if HEAD has captured run, restore from pinned commit
- Cache coverage is enforced invariant - missing cache entries fail hard in offline mode
- Optimizer determinacy validated by `tests/test_portfolio_opt.py`

---

*This handoff was created automatically at session start. Update as work progresses.*