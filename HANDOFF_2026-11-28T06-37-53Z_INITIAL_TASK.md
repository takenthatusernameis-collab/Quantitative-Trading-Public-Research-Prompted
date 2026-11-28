# Agentic Work Session Handoff

**Timestamp**: 2026-11-28T06:41:42Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py

# Skip slow batch/regression steps
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Files & Directories

- `experiments/*.json` - Canonical research artifacts (golden files)
- `ledger/RESEARCH_LEDGER.md` - Documented surviving validated strategies
- `data/` - Cached parquet data (gitignored except pinned vintages)
- `src/` - Core research scripts
- `scripts/` - Verification and utility scripts
- `.verify_snapshot/` - Gitignored backup directory for verification runs
- `.verify_reports/` - Gitignored extended verification reports

## Important Notes

1. **Seed**: Always use `SEED=42` for reproducibility
2. **Golden files**: `experiments/*.json` are committed artifacts - verification backs them up before re-running and restores them afterward
3. **Never commit verification output**: If a run is interrupted, restore with `--restore-only` before committing
4. **Cache coverage**: Enforced invariant - all data inputs must be pinned and tracked
5. **Optimizer determinicity**: Portfolio optimizer uses exact KKT active-set enumeration (E050 fix) for bit-reproducibility

## Next Session Suggestions

- Run `SEED=42 bash scripts/check.sh` to verify environment health
- Run `SEED=42 python3 run_all_verification.py --skip-slow` for quick validation
- Check `ledger/RESEARCH_LEDGER.md` for current strategy status
- Review any open issues in the verification pipeline