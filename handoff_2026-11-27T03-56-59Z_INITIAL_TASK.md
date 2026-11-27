# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-27T03:56:59Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State

- **Research Phase:** Complete (E001–E043)
- **Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Current Verification Status:** Ready for verification runs

## Quick Commands Reference

```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
# or
make verify
```

## Key Artifacts

- **Golden files:** `experiments/*.json` (canonical research artifacts)
- **Ledger:** `ledger/RESEARCH_LEDGER.md` (surviving validated strategies)
- **Data cache:** `data/` (gitignored except pinned vintages)
- **Backup location:** `.verify_snapshot/` (gitignored, with ACTIVE.json marker)

## Important Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
2. **Seed is always 42** for reproducibility
3. **Cache coverage is enforced** — `scripts/check_data_coverage.py` validates all data inputs
4. **No CI workflow can be created by agents** — maintainer must create via GitHub UI using template at `.github/workflow-templates/verification-gate.yml`

## Next Steps (if continuing)

- Run verification suite to confirm reproducibility
- Review any drift in extended verification report
- Check `ledger/golden_baseline.json` for pinned SHA-256 fingerprints

(End of file)
