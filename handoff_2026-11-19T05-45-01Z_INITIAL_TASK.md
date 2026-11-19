# Agentic Work Session Handoff

**Timestamp**: 2026-11-19T05:45:01Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
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

## Key Artifacts
- **Golden files**: `experiments/*.json` (committed artifacts, never modified by verification)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (surviving validated strategies)
- **Data cache**: `data/` (gitignored except pinned vintages)
- **Verification snapshot**: `.verify_snapshot/` (gitignored, for recovery)

## Important Notes
- Always use `SEED=42` for reproducibility
- Verification suite backs up golden files before re-running and restores them afterward
- If verification is interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` to recover
- Never commit verification output; restore goldens before committing
- Cache coverage is enforced: all `data.download()` calls must have pinned cache files

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Use `make verify-quick` for standard verification
4. Review any open items in the ledger (e.g., E041/E042 optimizer drift)
