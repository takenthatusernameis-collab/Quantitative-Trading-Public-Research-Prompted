# Agentic Work Session Handoff

**Timestamp**: 2026-11-16T04:43:16Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Notes
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts. Verification backs them up and restores after.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals pinned in `data/fundamentals/`.
- **Do not commit verification output** — restore before committing (`run_all_verification.py --restore-only`).
- **Optimizer determinism**: Tangency QP ill-conditioned; E041/E042 grid artifacts drift by 29-133 differences. Do not re-pin to silence.

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Use verification commands above as needed