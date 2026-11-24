# Agentic Work Session Handoff

**Timestamp:** 2026-11-24T11:05:42Z
**Session ID:** Initial handoff marker
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status
- **Research Phase:** Complete (E001–E043)
- **Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Verification Suite:** Ready for execution

## Quick Commands
```bash
# Convention robustness check (fast, offline)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min + E042 n_sim=50)
SEED=42 python3 run_all_verification.py --full
```

## Key Notes for Next Session
- All experiments are pre-registered with falsification expectations
- Golden files in `experiments/*.json` are canonical artifacts
- Verification suite backs up goldens before re-running and restores after
- **Never commit verification output** — restore with `--restore-only` if interrupted
- Data cache in `data/` (gitignored except pinned vintages)
- SEED=42 required for reproducibility

## Baseline Integrity Checks
- `scripts/check_goldens_clean.py` — working tree vs HEAD
- `scripts/check_golden_baseline.py` — artifacts vs SHA-256 in `ledger/golden_baseline.json`
- `scripts/check_data_coverage.py` — cache coverage invariant

---

*This handoff was created automatically to provide context for the next agentic work session.*
