# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T13:31:12Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. Research phase is complete.

**Key surviving validated strategies** are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
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

1. **Golden artifacts**: `experiments/*.json` are canonical research artifacts. The verification suite overwrites them during runs and restores them afterward. **Never leave a verification run half-finished.**

2. **Baseline integrity**:
   - `scripts/check_goldens_clean.py` compares working tree with HEAD
   - `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json`
   - Run `scripts/check.sh` before committing to catch mismatches

3. **Reproducibility**: Always use `SEED=42`. Cache coverage is enforced - all data inputs must be pinned.

4. **Recovery**: If verification interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

## Current State

- Research phase complete (E001–E043)
- All experiments have pre-registered JSON blocks with gates/falsification expectations
- Surviving strategies documented in ledger
- Verification suite validates 8 drivers in quick mode, 26 in extended, full grid in full mode

## Next Session Guidance

When resuming work:
1. Run `scripts/check.sh` to verify baseline integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Use `SEED=42` for all reproducibility
4. Never commit verification output - restore goldens first if interrupted

---
*This handoff was created automatically at session start for durability across agentic sessions.*