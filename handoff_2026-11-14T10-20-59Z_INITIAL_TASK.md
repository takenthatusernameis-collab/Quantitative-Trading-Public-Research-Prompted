# Agentic Work Session Handoff

**Timestamp**: 2026-11-14T10:23:58Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State

- **Research Phase**: Complete (E001–E043)
- **Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Current Baseline**: Golden artifacts in `experiments/*.json` are canonical

## Quick Start Commands

```bash
# Fast convention-robustness check (~seconds)
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

## Key Conventions

- **Seed**: Always use `SEED=42` for reproducibility
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Golden Files**: `experiments/*.json` are committed artifacts — never modified by verification
- **Recovery**: If verification interrupted, run `SEED=42 python3 run_all_verification.py --restore-only`

## Critical Notes

1. **Never leave verification half-finished** — it overwrites golden artifacts temporarily
2. **Check goldens before committing** — `scripts/check.sh` validates baseline integrity
3. **Cache coverage is enforced** — `scripts/check_data_coverage.py` validates all data inputs
4. **Optimizer determinism** — `src/portfolio_opt.py` validates on constraints, not solver status (ledger E049)

## Open Items (from Ledger)

- E041: 133 numeric differences remain (ill-conditioned QP, 1-ulp sensitivity) — do not re-pin
- E030: Now offline-reproducible since 2026-10-20 (pinned ETF panel)
- E029: Offline-reproducible (fundamentals pinned in `data/fundamentals/`)

## Next Steps

Run `SEED=42 bash scripts/check.sh` to verify environment integrity before proceeding.