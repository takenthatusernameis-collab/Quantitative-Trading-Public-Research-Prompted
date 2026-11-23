# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T17:42:28Z
**Session ID**: Initial handoff created for next agentic session
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status Summary

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. **Research phase is complete.** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Important Notes for Next Session

1. **Baseline Integrity**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them during re-runs and restores afterward. A verification run must never be left half-finished.

2. **Reproducibility**: Always use `SEED=42` (walk-forward + placebo RNG). Data cached in `data/` (gitignored except pinned vintages).

3. **Golden Files**: Committed artifacts in `experiments/*.json`. Never commit verification output — restore with `run_all_verification.py --restore-only` if interrupted.

4. **Ledger**: Check `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and their dispositions (REJECTED / PARTIAL / ACCEPTED).

5. **Data Coverage**: Cache coverage is an enforced invariant. Use `scripts/check_data_coverage.py` to verify.

## Next Steps for New Session

- Run `SEED=42 bash scripts/check.sh` to verify environment and baseline integrity
- Review `ledger/RESEARCH_LEDGER.md` for current strategy status
- Consider running `make verify-quick` for a full verification cycle
- Check for any new experiment ideas or follow-up analyses needed

---
*This handoff was created automatically to ensure continuity between agentic work sessions.*