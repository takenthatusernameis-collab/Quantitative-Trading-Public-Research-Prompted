# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T17:54:12Z
**Session**: Initial task message for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. Research phase is complete. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

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

## Critical Baseline Integrity Notes

- `experiments/*.json` are canonical research artifacts
- Verification suite overwrites them during re-run and restores afterward
- **Never leave a verification run half-finished** - it corrupts the baseline
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` - never re-pin without ledger entry

## Current State

- Research phase complete (E001–E043)
- All experiment drivers committed
- Verification suite operational
- Data caches pinned (2026-10-11/2026-10-12 vintages)
- E029 fundamentals pinned in `data/fundamentals/`
- E030 16-ETF panel committed
- E050 exact active-set enumeration fix applied (bit-reproducible optimizer)

## Next Steps for New Session

1. Run `make check` to verify baseline integrity
2. Run `make verify-quick` for quick validation
3. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
4. Any new experiments require pre-registration with falsification expectations

---
*This handoff was created automatically at session initialization.*