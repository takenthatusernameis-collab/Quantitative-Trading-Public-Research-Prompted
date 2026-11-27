# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-27T03:58:25Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State

- **Research Phase:** Complete (E001–E043)
- **Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Current Verification Status:** Ready for verification runs

## Quick Commands Reference

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
```

## Key Artifacts

- **Golden files:** `experiments/*.json`
- **Ledger:** `ledger/RESEARCH_LEDGER.md`
- **Data cache:** `data/`
- **Backup location:** `.verify_snapshot/`

## Important Notes

1. Never leave verification half-finished; restore with `--restore-only` or `git checkout -- experiments/`
2. Seed is always 42
3. Cache coverage enforced by `scripts/check_data_coverage.py`
4. No CI workflow can be created by agents

## Next Steps (if continuing)

- Run verification suite to confirm reproducibility
- Review drift in extended verification report
- Check `ledger/golden_baseline.json` for pinned SHA-256 fingerprints

(End of file)
