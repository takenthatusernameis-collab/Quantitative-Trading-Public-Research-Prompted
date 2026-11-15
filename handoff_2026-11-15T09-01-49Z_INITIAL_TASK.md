# Handoff — Agentic Work Session

**Timestamp:** 2026-11-15T09:07:03Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Phase:** Research complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

## Key Artifacts
- **Golden baselines:** `experiments/*.json` (canonical research artifacts)
- **Ledger:** `ledger/RESEARCH_LEDGER.md` (validated strategies)
- **Golden fingerprints:** `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- **Data cache:** `data/` (parquet, gitignored except pinned vintages)
- **Fundamentals snapshot:** `data/fundamentals/` (pinned for E029)

## Integrity Notes
- Verification overwrites `experiments/*.json` then restores — never leave a run half-finished
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against baseline drift
- Cache coverage enforced: `scripts/check_data_coverage.py` (update with `--update` when adding inputs)

## Known Drift (reporting only, do not re-pin)
- **E030:** 28 numeric diffs on near-zero quantities (yfinance non-reproducible; panel now committed)
- **E041:** 133 numeric diffs (1-ulp QP ill-conditioning, optimizer fixed; 3 structural diffs resolved)
- **E042/E041 grid:** 29–133 numeric diffs (same QP ill-conditioning)
- See ledger entries E045, E048, E049 for details

## Next Session Priorities
1. Run verification suite to confirm current state
2. Review any failed gates or new drift
3. Continue from ledger open items (E041 QP ill-conditioning, E042 confirmatory)

---
*Generated automatically at session start. Update this file before ending your session.*