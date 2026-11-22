# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T23:34:00Z
**Session ID**: Initial handoff created by user request
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository on 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

```bash
# Fast convention-robustness check + template validation
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

- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are committed artifacts - never commit verification output
- **Recovery**: If verification is interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.

## Next Steps for New Session

1. Run `make check` to verify baseline integrity
2. Run `make verify-quick` for quick verification
3. Review `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
4. Check for any open items in the ledger (e.g., E041 optimizer drift, E049 portfolio optimizer determinism)

## Current State

- Research phase: COMPLETE (E001–E043)
- Verification suite: Operational with quick/extended/full modes
- Baseline integrity: Protected by `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py`
- CI template: Available at `.github/workflow-templates/verification-gate.yml` (requires manual creation)
