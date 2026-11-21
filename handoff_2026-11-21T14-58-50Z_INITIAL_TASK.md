# Agentic Work Session Handoff

**Timestamp**: 2026-11-21T14:59:21Z
**Session ID**: Initial handoff created by Kilo
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Artifacts
- **Golden files**: `experiments/*.json` (committed artifacts, never modified by verification)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (surviving validated strategies)
- **Data cache**: `data/` (gitignored except pinned vintages)
- **Verification reports**: `.verify_reports/` (gitignored, written outside `experiments/`)

## Critical Notes
1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores them after. Use `--restore-only` if interrupted.
2. **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against accidental baseline replacement.
3. **Data coverage**: All `data.download()` call sites must have pinned cache files (enforced by `scripts/check_data_coverage.py`).
4. **Optimizer determinacy**: `src/portfolio_opt.py` validates on constraints, not solver exit status (ledger E049).
5. **SEED=42** always for reproducibility.

## Next Steps for New Session
- Run `SEED=42 bash scripts/check.sh` to verify environment
- Check `ledger/RESEARCH_LEDGER.md` for current strategy status
- Review any open items in the ledger (E041 drift, E042 sensitivity grid, etc.)