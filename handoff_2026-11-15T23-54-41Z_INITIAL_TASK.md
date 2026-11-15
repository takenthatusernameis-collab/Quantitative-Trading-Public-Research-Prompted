# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T23:54:41Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Verification Commands
```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh
# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Files
- `ledger/RESEARCH_LEDGER.md` - Validated strategies
- `experiments/*.json` - Canonical research artifacts (golden files)
- `scripts/check.sh` - Convention robustness check
- `run_all_verification.py` - Full verification suite
- `AGENTS.md` - Project commands & conventions

## Important Notes
- Golden files in `experiments/` are committed artifacts — verification overwrites and restores them
- Never commit verification output; use `--restore-only` to recover if interrupted
- Seed must always be `SEED=42` for reproducibility
- Data cached in `data/` (gitignored except pinned vintages)