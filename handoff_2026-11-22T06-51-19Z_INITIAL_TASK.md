# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T06:52:31Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
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

## Key Artifacts
- **Golden files**: `experiments/*.json` (committed artifacts, never modified by verification)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (validated strategies & dispositions)
- **Data cache**: `data/` (gitignored except pinned vintages)
- **Verification snapshot**: `.verify_snapshot/` (gitignored, recovery mechanism)

## Important Notes
- Always use `SEED=42` for reproducibility
- Verification suite backs up goldens before re-running and restores them afterward
- Never commit verification output — restore with `--restore-only` if interrupted
- Cache coverage is enforced: all data inputs must be pinned in `ledger/data_baseline.json`
- Optimizer determinacy issue in E041/E042 (see ledger E049) — do not re-pin to silence drift

## Next Steps
- Run `SEED=42 bash scripts/check.sh` to verify environment integrity
- Consult `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
- Check `AGENTS.md` for full command reference and conventions