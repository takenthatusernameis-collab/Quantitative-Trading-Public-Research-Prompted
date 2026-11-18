# Agentic Work Session Handoff

**Timestamp**: 2026-11-18T05:57:30Z
**Session ID**: Initial handoff for next agentic work session
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

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts. The verification suite backs them up before re-running and restores them afterward.
- **Do not commit verification output**: If a run is interrupted, restore before committing (`run_all_verification.py --restore-only`).
- **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` are first-class steps in `scripts/check.sh` that verify artifact integrity.

## Current State

- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All verification commands tested and working
- Data cached in `data/` (gitignored except pinned vintages)

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Run `SEED=42 python3 run_all_verification.py` for quick verification
3. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
4. Review any open items in the ledger (e.g., E041 optimizer drift, E049 open items)

## Key Files to Reference

- `AGENTS.md` - Project commands & conventions
- `ledger/RESEARCH_LEDGER.md` - Validated strategies and dispositions
- `ledger/golden_baseline.json` - Pinned SHA-256 fingerprints for golden artifacts
- `ledger/data_baseline.json` - Pinned SHA-256 fingerprints for data artifacts
- `scripts/check.sh` - Fast convention-robustness check
- `run_all_verification.py` - Main verification suite