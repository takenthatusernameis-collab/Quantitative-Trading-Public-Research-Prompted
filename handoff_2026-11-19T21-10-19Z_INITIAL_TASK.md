# Agentic Work Session Handoff

**Timestamp**: 2026-11-19T21:11:42Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043)**. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Important Notes

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts. The verification suite backs them up before re-running and restores them afterward.
- **Do not commit verification output**: If a run is interrupted, restore with `run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.

## Current State

- Research phase complete (E001–E043)
- Ledger documents surviving validated strategies
- Verification suite is the primary gate for any changes
- No active work in progress - clean handoff point

## Next Steps for New Session

1. Run `make check` to verify baseline integrity
2. Review `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Check `scripts/check_golden_baseline.py` and `scripts/check_data_coverage.py` for any drift
4. Proceed with any new experiment design or verification tasks