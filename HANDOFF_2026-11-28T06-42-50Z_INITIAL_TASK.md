# Agentic Work Session Handoff

**Timestamp**: 2026-11-28T08:40:07Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Notes for Next Session
- Baseline integrity: `experiments/*.json` are canonical artifacts. Verification suite backs them up to `.verify_snapshot/` and restores after.
- If interrupted, recover with: `SEED=42 python3 run_all_verification.py --restore-only`
- Seed must always be `SEED=42` for reproducibility
- Data cached in `data/` (gitignored except pinned vintages)
- Dependencies: `pip install -r requirements.txt`

## Recent Verification Status
Per AGENTS.md (measured 2026-11-23T05:17Z):
- All 18 extended drivers reproduce with 0 differences (numeric_tol=1e-4)
- E029, E030, E041 now bit-reproducible after E050 exact-solver fix
- E042 min-var confirmatory: PARTIAL (3/5 gates pass)

## Next Steps (if continuing)
1. Run `make check` to verify baseline integrity
2. Run `make verify-quick` for fast verification
3. Check `ledger/RESEARCH_LEDGER.md` for current experiment dispositions