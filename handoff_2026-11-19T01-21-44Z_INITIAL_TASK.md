# Agentic Work Session Handoff

**Timestamp**: 2026-11-19T01:34:37Z
**Session**: Initial handoff for next agentic work session

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
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

## Key Integrity Notes
- `experiments/*.json` are canonical research artifacts
- Verification suite backs up goldens to `.verify_snapshot/` and restores after
- Never leave a verification run half-finished
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only`
- Golden baseline pinned in `ledger/golden_baseline.json` — do not re-pin without explicit update

## Current State
- Repository clean, no active verification runs
- All experiments committed through E043
- Ledger documents surviving strategies
- Data vintages pinned (2026-10-12, 2026-10-11, fundamentals)

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Use `make verify-quick` for fast validation
4. Review any open items in ledger (E049 optimizer determinism, E041 drift)