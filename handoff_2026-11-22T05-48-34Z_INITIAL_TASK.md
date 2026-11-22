# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T05:49:19Z
**Session ID**: Initial handoff for next session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Files

- `AGENTS.md` - Project commands & conventions (read first)
- `ledger/RESEARCH_LEDGER.md` - Validated strategies documentation
- `experiments/*.json` - Canonical research artifacts (golden files)
- `scripts/check.sh` - Convention robustness check
- `run_all_verification.py` - Main verification suite
- `src/batch_run.py` - Batch experiment runner
- `src/validate.py` - Validation script

## Verification Suite Notes

- The verification suite overwrites `experiments/*.json` while re-running drivers and restores them afterwards
- A verification run must never be left half-finished
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline integrity enforced via `ledger/golden_baseline.json` (SHA-256 pinned)

## Current State

No active verification run in progress. Repository is at a clean state ready for next work session.

## Next Steps for New Session

1. Run `make check` to verify convention robustness
2. Run `make verify-quick` for quick verification if needed
3. Consult `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Check `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` for baseline integrity