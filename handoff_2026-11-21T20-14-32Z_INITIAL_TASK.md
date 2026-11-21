# Agentic Work Session Handoff

**Timestamp**: 2026-11-21T21:08:05Z
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

## Key Integrity Notes
- `experiments/*.json` are canonical research artifacts — verification overwrites and restores them
- Never leave a verification run half-finished; use `--restore-only` to recover
- Golden baseline pinned in `ledger/golden_baseline.json` — never re-pin as side effect of verification
- Cache coverage enforced via `scripts/check_data_coverage.py` and `ledger/data_baseline.json`

## Next Session Starting Point
Run `SEED=42 bash scripts/check.sh` to verify environment integrity before proceeding with any experiments or verification runs.