# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T20:40:00Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Current State

- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates
- Golden artifacts in `experiments/*.json` are canonical baselines

## Verification Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
```

## Key Conventions

- Seed: SEED=42
- Primary convention: close-to-close (v1.2.3)
- Data: cached parquet in data/ (pinned vintages only)
- Offline mode: QUANT_RESEARCH_OFFLINE=1
- Golden files: never modified by verification; restored after re-run

## Important Notes

- Verification backs up goldens to .verify_snapshot/ before re-running and restores after
- Never leave a verification run half-finished
- Recovery: SEED=42 python3 run_all_verification.py --restore-only or git checkout -- experiments/
- Baseline guards: scripts/check_goldens_clean.py and scripts/check_golden_baseline.py
- CI gate template: .github/workflow-templates/verification-gate.yml

## Next Steps

Resume verification, run experiments, or continue research from the ledger's current disposition.
