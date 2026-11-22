# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T20:46:33Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Verification suite operational with multiple tiers (check, verify-quick, verify-extended, verify-full)

## Key Commands for Next Session
```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes
- **Never leave verification half-finished** - it overwrites `experiments/*.json` and restores after
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` - never re-pin as side effect of verification
- Cache coverage enforced: `scripts/check_data_coverage.py` validates all data inputs
- SEED=42 required for reproducibility (walk-forward + placebo RNG)

## Current State
- No active verification run detected
- Ready for next experiment or verification run