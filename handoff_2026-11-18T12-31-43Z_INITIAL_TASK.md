# Agentic Work Session Handoff

**Timestamp**: 2026-11-18T12:39:22Z
**Session ID**: Initial handoff for next agentic work session
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

## Key Verification Notes
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts - never commit verification output
- **Recovery**: If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only`
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Offline mode**: `QUANT_RESEARCH_OFFLINE=1` enforced during verification

## Baseline Integrity
- `scripts/check_goldens_clean.py` - compares working tree with HEAD
- `scripts/check_golden_baseline.py` - compares with SHA-256 in `ledger/golden_baseline.json`
- `scripts/check_data_coverage.py` - validates all cache files exist and match pinned SHA-256

## Current State
- Research phase complete (E001–E043)
- Ledger at `ledger/RESEARCH_LEDGER.md` documents surviving strategies
- Verification suite validates reproducibility across 26 experiment drivers
- E042 (min-var confirmatory) is PARTIAL; E025, E041 REJECTED

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Run verification suite as needed: `make verify-quick`, `make verify-extended`, or `make verify-full`
4. Any new experiments require pre-registration with falsification expectations

---
*This handoff was created automatically at session start.*