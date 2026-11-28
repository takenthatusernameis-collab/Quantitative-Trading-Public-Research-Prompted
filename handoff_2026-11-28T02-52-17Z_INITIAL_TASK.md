# Agentic Work Session Handoff

**Timestamp**: 2026-11-28T02:54:16Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Artifacts
- **Golden files**: `experiments/*.json` (committed canonical artifacts)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (validated strategies)
- **Data cache**: `data/` (gitignored parquet, pinned vintages in `data/vintages.json`)
- **Fundamentals**: `data/fundamentals/` (pinned per `data/fundamentals_vintages.json`)

## Verification Suite Notes
- `run_all_verification.py` backs up golden files before re-running, restores after
- Never leave a verification run half-finished (baseline integrity)
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- `scripts/check_golden_baseline.py` compares artifacts to SHA-256 in `ledger/golden_baseline.json`
- Cache coverage enforced via `scripts/check_data_coverage.py` (must match `ledger/data_baseline.json`)

## Current State
- Research phase complete (E001–E043)
- All experiment drivers committed
- Golden baseline pinned and verified
- E042 (min-var confirmatory): PARTIAL
- E041 (market-neutral portfolio): REJECTED
- E025 (cointegration stat-arb): REJECTED

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Review `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Use `make verify-quick` for fast validation
4. Any new experiments require pre-registration with falsification expectations