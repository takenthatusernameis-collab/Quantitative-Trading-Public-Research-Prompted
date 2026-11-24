# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T16:12:27Z
**Session ID**: Initial handoff created for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Conventions

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Convention**: Close-to-close is v1.2.3 primary; overnight decomposition reported alongside
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Golden files**: `experiments/*.json` are committed artifacts - never modified by verification
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` if interrupted

## Current State

- Research phase complete (E001–E043)
- Verification suite operational
- Ledger documents surviving strategies
- No active experiments running

## Next Session Guidance

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Use verification commands above to reproduce results
4. Any new experiments require pre-registration with falsification expectations

---
*This handoff was created automatically to provide durable context for the next agentic work session.*