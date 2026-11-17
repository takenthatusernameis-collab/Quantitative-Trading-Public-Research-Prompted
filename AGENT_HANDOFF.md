# Agent Handoff - Initial Task Message

**Timestamp:** 2026-11-17T11:55:19Z
**Session:** Initial task message for next agentic work session

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Integrity Notes
- `experiments/*.json` are canonical research artifacts
- Verification suite overwrites them while re-running drivers and restores afterwards
- **Never leave a verification run half-finished** - use `--restore-only` to recover
- Golden baseline pinned in `ledger/golden_baseline.json` - never re-pin as side effect of verification
- Cache coverage enforced: `scripts/check_data_coverage.py` validates all data inputs

## Next Session Guidance
Run `make check` first to verify environment integrity, then proceed with verification tasks as needed.