# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T01:29:56Z
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

## Key Files
- `ledger/RESEARCH_LEDGER.md` - Documented surviving validated strategies
- `experiments/*.json` - Canonical research artifacts (golden files)
- `data/vintages.json` - Pinned data vintage (2026-10-12)
- `data/fundamentals_vintages.json` - Pinned fundamentals for E029
- `ledger/golden_baseline.json` - SHA-256 fingerprints of golden artifacts
- `ledger/data_baseline.json` - SHA-256 fingerprints of data files

## Important Notes
- **Always use `SEED=42`** for reproducibility
- Golden files in `experiments/` are committed artifacts - verification suite backs them up before re-running and restores them afterward
- Never commit verification output; if interrupted, restore with `run_all_verification.py --restore-only`
- Cache coverage is enforced invariant - all data downloads must be pinned

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Use `make verify-quick` for standard verification
4. Refer to AGENTS.md for full project conventions and commands