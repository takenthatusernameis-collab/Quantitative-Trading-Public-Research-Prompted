# Agentic Work Session Handoff

**Timestamp:** 2026-11-20T05:29:23Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands for Next Session
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

## Current State
- Repository is a git repo with committed golden artifacts in `experiments/*.json`
- Data cached in `data/` (gitignored except pinned vintages)
- Verification suite backs up goldens before re-running and restores after
- **Critical:** Never leave a verification run half-finished; use `--restore-only` to recover if interrupted

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. Run verification suite as needed (`verify-quick`, `verify-extended`, or `verify-full`)
3. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
4. Any new experiments require pre-registration with falsification expectations

## Important Notes
- Golden files in `experiments/` are canonical artifacts — do not modify without re-pinning via `check_golden_baseline.py --update`
- Cache coverage is enforced: `scripts/check_data_coverage.py` validates all data inputs
- Optimizer determinacy issue tracked in ledger E049 (SLSQP status-gating removed, but 1-ulp sensitivity remains)
- CI workflow template at `.github/workflow-templates/verification-gate.yml` (maintainer must create actual workflow)

---
*Generated automatically for session continuity*