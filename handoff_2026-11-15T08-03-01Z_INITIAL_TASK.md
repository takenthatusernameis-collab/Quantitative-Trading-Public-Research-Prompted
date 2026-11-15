# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T08:05:33Z
**Session ID**: Initial handoff
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

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

## Critical Notes

- **Never leave verification half-finished**: The suite backs up `experiments/*.json` to `.verify_snapshot/` and restores after. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Golden baseline integrity**: `ledger/golden_baseline.json` pins SHA-256 of canonical artifacts. Do not re-pin without explicit ledger entry.
- **Data coverage invariant**: All `data.download()` calls must have pinned cache files matching `ledger/data_baseline.json`. Run `scripts/check_data_coverage.py --update` to add new inputs.
- **Optimizer determinacy**: `src/portfolio_opt.py` validates on problem constraints, not solver exit status (ledger E049). E041/E042 grid artifacts have known 1-ulp drift — do not re-pin to silence.
- **Seed**: Always use `SEED=42` for reproducibility.

## Current State

- Research phase complete (E001–E043)
- Ledger documents surviving validated strategies
- Verification suite operational
- No active experiment in progress

## Next Steps for New Session

1. Run `make check` to verify baseline integrity
2. Review `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Check `scripts/check_golden_baseline.py` and `scripts/check_data_coverage.py` for any drift alerts
4. Proceed with any new experiment design or verification tasks