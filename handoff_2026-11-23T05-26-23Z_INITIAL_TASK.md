# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T05:28:48Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Current State
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates

## Quick Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Artifacts
- **Golden files**: `experiments/*.json` (canonical research artifacts)
- **Data cache**: `data/` (gitignored except pinned vintages 2026-10-11, 2026-10-12)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (dispositions, decisions, fixes)
- **Data baseline**: `ledger/data_baseline.json` (SHA-256 pinned cache files)
- **Golden baseline**: `ledger/golden_baseline.json` (SHA-256 pinned experiment outputs)

## Integrity Guards
- `scripts/check_goldens_clean.py` - detects working tree vs HEAD divergence
- `scripts/check_golden_baseline.py` - detects committed baseline replacement
- `scripts/check_data_coverage.py` - enforces cache coverage invariant
- `tests/test_portfolio_opt.py` - validates optimizer determinism

## Recovery
If verification interrupted:
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

## Next Session Priority
- Review any open items in `ledger/RESEARCH_LEDGER.md`
- Run `make check` to verify baseline integrity
- Consider `verify-extended` or `verify-full` for deeper validation