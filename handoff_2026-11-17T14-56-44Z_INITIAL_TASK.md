# Agentic Work Session Handoff

**Timestamp**: 2026-11-17T15:50:31Z
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
- `run_all_verification.py` - Main verification suite
- `scripts/check.sh` - Fast convention-robustness check
- `AGENTS.md` - Project commands & conventions

## Important Notes
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts. Verification backs them up before re-running and restores them afterward.
- **Do not commit verification output**: If a run is interrupted, restore with `run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Cache coverage**: Enforced invariant - all data inputs must be pinned in `ledger/data_baseline.json`
- **E029 fundamentals**: Separately pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` - fully offline-reproducible
- **Optimizer determinacy**: `src/portfolio_opt.py` validates solver answer on problem constraints, not solver exit status (ledger E049)

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current research status
3. Determine if verification runs are needed (`verify-quick`, `verify-extended`, `verify-full`)
4. Any new experiments must follow pre-registration protocol with falsification expectations