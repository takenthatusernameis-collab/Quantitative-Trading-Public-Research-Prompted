# Agentic Work Session Handoff

**Timestamp:** 2026-11-10T05:19:06Z
**Session ID:** Initial handoff for next agentic work session
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Project Conventions

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Convention**: Close-to-close is the v1.2.3 primary convention. Overnight decomposition is reported alongside for every strategy.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). The 2026-10-12 vintage is pinned in `data/vintages.json`; the 2026-10-11 vintage is committed.
- **Golden files**: `experiments/*.json` are committed artifacts. The verification suite backs them up before re-running and restores them afterward.
- **Do not commit verification output**: If a run is interrupted, restore before committing (`run_all_verification.py --restore-only` or `git checkout -- experiments/`).

## Current Status

- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Verification suite operational with multiple tiers (check, verify-quick, verify-extended, verify-full)
- Baseline integrity maintained via `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py`

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
3. Run appropriate verification tier based on needs
4. Check for any open items in the ledger (e.g., E041 optimizer determinism, E042 grid artifacts)

---

*This handoff file is durable and will persist across sessions.*