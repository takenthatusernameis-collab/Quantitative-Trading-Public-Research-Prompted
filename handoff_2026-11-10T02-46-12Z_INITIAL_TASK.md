# Agentic Work Session Handoff

**Timestamp:** 2026-11-10T03:33:27Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative-Trading-Public-Research-Prompted

## Session Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are canonical artifacts - verification backs them up and restores them
- **Do not commit verification output** - restore before committing with `--restore-only`
- **Cache coverage is enforced** - `scripts/check_data_coverage.py` validates all data downloads
- **Optimizer determinacy**: SLSQP status 8 at constrained optimum is valid (ledger E049)

## Next Steps

Resume verification or continue from ledger entries E045-E049.