# Agentic Work Session Handoff

**Timestamp:** 2026-11-28T05:32:39Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

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

## Baseline Integrity Notes

- `experiments/*.json` are canonical research artifacts
- Verification suite backs up goldens to `.verify_snapshot/` before re-running and restores after
- Never leave a verification run half-finished
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` (SHA-256 fingerprints)

## Reproducibility

- **Seed**: Always use `SEED=42`
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Cache coverage**: Enforced invariant via `scripts/check_data_coverage.py`
- **Dependencies**: `pip install -r requirements.txt`

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current experiment dispositions
3. Run verification suite as needed (`verify-quick`, `verify-extended`, `verify-full`)
4. Any new experiments must follow pre-registration protocol with falsification expectations

## Important Files

- `AGENTS.md` - Project commands & conventions (this file's source)
- `ledger/RESEARCH_LEDGER.md` - Experiment dispositions and evidence
- `ledger/golden_baseline.json` - SHA-256 pinned golden artifacts
- `ledger/data_baseline.json` - SHA-256 pinned data cache files
- `scripts/check.sh` - Fast convention-robustness check
- `run_all_verification.py` - Full verification suite