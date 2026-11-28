# Agentic Work Session Handoff

**Timestamp**: 2026-11-28T06:32:22Z
**Session**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Important Notes

- **Golden files**: `experiments/*.json` are committed artifacts. The verification suite backs them up before re-running and restores them afterward — the baseline is never modified by verification.
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG).
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). The 2026-10-12 vintage is pinned in `data/vintages.json`.
- **Baseline Integrity**: A verification run must never be left half-finished. If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` to recover golden artifacts.
- **Do not commit verification output**: If a run is interrupted, restore before committing.

## Next Steps for New Session

1. Run `make check` to verify the environment and baseline integrity
2. Review `ledger/RESEARCH_LEDGER.md` for surviving validated strategies
3. Check `scripts/check.sh` output for any golden mismatches before proceeding
4. Use the verification commands above as needed for reproduction/verification