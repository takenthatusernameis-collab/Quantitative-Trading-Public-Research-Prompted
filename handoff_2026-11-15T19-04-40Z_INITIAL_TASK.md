# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T19:05:54Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Critical Notes

- **Never leave a verification run half-finished** — it overwrites `experiments/*.json` and restores them after. Use `--restore-only` to recover if interrupted.
- **Golden baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against accidental baseline replacement.
- **Data coverage invariant**: All `data.download()` call sites must have cached, git-tracked files matching SHA-256 in `ledger/data_baseline.json`.
- **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.
- **E029/E030/E041**: Have known offline-reproducibility considerations (see AGENTS.md for details).

## Next Steps

Resume verification or run individual experiment drivers as needed. Check `ledger/RESEARCH_LEDGER.md` for current disposition of all experiments (E001–E043).