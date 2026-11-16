# Handoff for Next Agentic Work Session

**Timestamp:** 2026-11-16T10:47:27Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Golden artifacts in `experiments/*.json` are canonical baselines

## Verification Commands (SEED=42 required)
```bash
# Fast convention-robustness check (~seconds)
make check

# Quick full verification (~8 min)
make verify-quick

# Extended verification (~21 min)
make verify-extended

# Full verification (~15 min)
make verify-full
```

## Key Constraints
- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` — never re-pin as side effect of verification
- Data cache coverage enforced via `scripts/check_data_coverage.py` and `ledger/data_baseline.json`

## Current Status
No active verification run. Workspace is clean and ready for next task.