# Agentic Work Session Handoff

**Timestamp:** 2026-11-12T02:22:04Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands

```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Conventions

- **Seed:** Always use `SEED=42`
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages)
- **Golden files:** `experiments/*.json` are committed artifacts — never modified by verification
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only` if interrupted

## Next Steps

1. Run `scripts/check.sh` to verify baseline integrity
2. Execute verification suite as needed
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Check `.verify_reports/` for any drift reports from extended runs

## Important Notes

- Verification suite overwrites `experiments/*.json` during run and restores after — never leave a run half-finished
- `scripts/check_golden_baseline.py` validates against pinned SHA-256 in `ledger/golden_baseline.json`
- Cache coverage is enforced via `scripts/check_data_coverage.py`