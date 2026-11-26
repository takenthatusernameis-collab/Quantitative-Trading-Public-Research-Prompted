# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T02:35:01Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
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

## Key Artifacts
- **Golden files**: `experiments/*.json` (committed artifacts, never modified by verification)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (documented surviving strategies)
- **Data cache**: `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages)
- **Fundamentals**: `data/fundamentals/` (pinned per `data/fundamentals_vintages.json`)

## Verification Suite Notes
- `run_all_verification.py` backs up golden files before re-running and restores them afterward
- If interrupted, recover with: `SEED=42 python3 run_all_verification.py --restore-only`
- Convention: Close-to-close is v1.2.3 primary; overnight decomposition reported alongside
- Seed: Always use `SEED=42` (walk-forward + placebo RNG)

## Next Session Starting Point
Ready to continue verification, run experiments, or investigate any open items from the ledger.