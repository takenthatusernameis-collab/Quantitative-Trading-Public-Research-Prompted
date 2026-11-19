# Agentic Work Session Handoff

**Timestamp**: 2026-11-19T02:37:00Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
```

## Key Artifacts
- `experiments/*.json` - Canonical research artifacts (golden files)
- `ledger/RESEARCH_LEDGER.md` - Documented surviving strategies
- `ledger/golden_baseline.json` - SHA-256 fingerprints of golden artifacts
- `data/vintages.json` - Pinned data cache versions
- `data/fundamentals_vintages.json` - Pinned fundamentals snapshot

## Critical Rules
1. Never leave verification half-finished - it overwrites golden files and must restore them
2. Always use SEED=42 for reproducibility
3. Do not commit verification output - restore goldens first with `--restore-only`
4. Cache coverage is enforced - all data inputs must be pinned in `ledger/data_baseline.json`

## Recent State
- Research phase complete (E001–E043)
- E025, E041: REJECTED
- E042: PARTIAL (min-var confirmatory)
- E029, E030: Now offline-reproducible with pinned data (since 2026-10-20)
- Optimizer determinism issue documented in ledger E049 (ill-conditioned QP)

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Consider running `make verify-quick` to validate current state
4. Any new experiments must follow pre-registration protocol

---
*This handoff was created automatically at session start. Update as needed.*
