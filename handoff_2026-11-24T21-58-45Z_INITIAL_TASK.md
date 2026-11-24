# Agentic Work Session Handoff

**Timestamp:** 2026-11-24T22:07:47Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
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

## Key Artifacts
- **Golden files:** `experiments/*.json` (canonical research artifacts)
- **Ledger:** `ledger/RESEARCH_LEDGER.md` (validated strategies)
- **Data cache:** `data/` (gitignored except pinned vintages)
- **Verification snapshot:** `.verify_snapshot/` (gitignored, recovery mechanism)

## Important Notes
- Always use `SEED=42` for reproducibility
- Verification suite backs up goldens before re-running and restores them afterward
- Never commit verification output — restore with `run_all_verification.py --restore-only` if interrupted
- Cache coverage is enforced: `scripts/check_data_coverage.py` validates all data inputs
- Optimizer determinism fixed in E050 (exact KKT active-set enumeration)

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Review any open issues or planned experiments
4. Consider running `make verify-quick` to confirm baseline reproducibility