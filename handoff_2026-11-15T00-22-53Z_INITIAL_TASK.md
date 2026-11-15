# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T00:25:29Z
**Session ID**: Initial session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Files
- `ledger/RESEARCH_LEDGER.md` - Documented surviving validated strategies
- `experiments/*.json` - Canonical research artifacts (golden files)
- `scripts/check.sh` - Convention robustness check
- `run_all_verification.py` - Main verification suite
- `AGENTS.md` - Project commands & conventions

## Important Notes
- Golden files in `experiments/` are committed artifacts - never commit verification output
- Use `SEED=42` for reproducibility
- Cache coverage is enforced - all data inputs must be pinned
- If verification is interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` to recover

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Determine if any experiments need re-running or new research to begin