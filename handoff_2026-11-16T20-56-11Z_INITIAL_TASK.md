# Agentic Work Session Handoff

**Timestamp**: 2026-11-16T20:58:16Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State

- **Research Phase**: Complete (E001–E043)
- **Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Current Baseline**: Golden artifacts in `experiments/*.json` are canonical

## Quick Commands Reference

```bash
# Fast convention-robustness check (~seconds, offline)
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

## Critical Integrity Notes

1. **Never leave verification half-finished** - it overwrites `experiments/*.json` and restores them after. Use `--restore-only` to recover if interrupted.
2. **Golden baseline pinned in** `ledger/golden_baseline.json` - do not re-pin without ledger entry.
3. **Data cache coverage enforced** - `scripts/check_data_coverage.py` validates all cache entries match `ledger/data_baseline.json`.
4. **Offline mode required** - `QUANT_RESEARCH_OFFLINE=1` during verification to prevent live downloads.

## Key Files to Understand

- `AGENTS.md` - Project commands & conventions (this file's instructions)
- `ledger/RESEARCH_LEDGER.md` - Surviving validated strategies
- `ledger/golden_baseline.json` - SHA-256 pinned artifact fingerprints
- `ledger/data_baseline.json` - SHA-256 pinned data cache fingerprints
- `scripts/check_goldens_clean.py` - Working tree vs HEAD check
- `scripts/check_golden_baseline.py` - Working tree vs pinned baseline check
- `scripts/check_data_coverage.py` - Data cache completeness check

## Next Session Suggested Starting Points

- Run `make check` to verify baseline integrity before any changes
- Review `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
- Check if any open items in ledger need attention (E041 optimizer drift, E042 sensitivity grid)

---
*This handoff was created automatically at session start. Update as needed during work.*