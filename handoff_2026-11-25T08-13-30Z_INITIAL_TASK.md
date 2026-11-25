# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T08:19:01Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

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

## Key Notes

- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are canonical artifacts - never commit verification output
- **Verification suite**: Backs up goldens before re-running and restores them afterward
- **If interrupted**: Run `SEED=42 python3 run_all_verification.py --restore-only` to recover
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Dependencies**: `pip install -r requirements.txt`

## Critical Baseline Integrity

- `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` are first-class steps in verification
- Never re-pin artifacts to "silence" tolerance violations - only deliberate code changes recorded in ledger warrant re-pinning
- E041/E042 are now bit-reproducible after E050 exact-solver fix (commit `72dc947`)

## Next Session Suggestions

1. Run `make check` to verify baseline integrity
2. Run `make verify-quick` for fast verification
3. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
4. Review any open issues in the ledger for potential follow-up experiments