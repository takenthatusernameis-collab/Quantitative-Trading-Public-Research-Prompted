# Agentic Work Session Handoff

**Timestamp**: 2026-11-17T21:49:30Z
**Session ID**: Initial handoff created for next agentic session
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

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

## Critical Integrity Notes

1. **Golden files**: `experiments/*.json` are canonical research artifacts. The verification suite backs them up before re-running and restores them afterward.
2. **Never commit verification output**: If a run is interrupted, restore with `run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against unauthorized baseline changes
4. **Seed**: Always use `SEED=42` for reproducibility
5. **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`

## Current State

- Research phase complete (E001–E043)
- All experiment drivers in `experiments/` directory
- Verification suite in `run_all_verification.py`
- Ledger of results in `ledger/RESEARCH_LEDGER.md`

## Next Steps for New Session

1. Run `make check` to verify convention robustness
2. Run `make verify-quick` for quick full verification
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Check `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` for any baseline drift warnings

## Important Files

- `AGENTS.md` - Project commands & conventions (this file's instructions)
- `ledger/RESEARCH_LEDGER.md` - Documented surviving strategies
- `ledger/golden_baseline.json` - SHA-256 fingerprints of canonical artifacts
- `scripts/check.sh` - Fast convention-robustness check
- `run_all_verification.py` - Main verification orchestration
- `experiments/*.json` - Canonical golden artifacts (do not modify directly)

---
*This handoff was created automatically to ensure continuity between agentic work sessions.*