# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T20:39:04Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Current State

- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates
- Golden artifacts in `experiments/*.json` are canonical baselines

## Verification Commands

```bash
# Fast convention-robustness check (~seconds, offline)
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
```

## Key Conventions

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Convention**: Close-to-close is v1.2.3 primary; overnight decomposition reported alongside
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Offline mode**: Verification runs with `QUANT_RESEARCH_OFFLINE=1`
- **Golden files**: Never modified by verification; restored after re-run

## Important Notes

- Verification suite backs up goldens to `.verify_snapshot/` before re-running and restores after
- Never leave a verification run half-finished (goldens would be overwritten)
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard baseline integrity
- CI gate template at `.github/workflow-templates/verification-gate.yml` (maintainer must create actual workflow)

## Next Steps

Resume verification, run experiments, or continue research from the ledger's current disposition.
