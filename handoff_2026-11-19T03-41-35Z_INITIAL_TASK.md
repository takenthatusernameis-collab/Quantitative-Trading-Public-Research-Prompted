# Agentic Work Session Handoff

**Timestamp**: 2026-11-19T03:42:31Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Convention robustness check (fast, offline)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min + E042 n_sim=50)
SEED=42 python3 run_all_verification.py --full
```

## Key Artifacts
- **Golden files**: `experiments/*.json` (committed canonical artifacts)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (validated strategies)
- **Data cache**: `data/` (gitignored, pinned vintages in `data/vintages.json`)
- **Golden baseline**: `ledger/golden_baseline.json` (SHA-256 fingerprints)

## Important Notes
- Never leave a verification run half-finished (goldens are overwritten during run, restored after)
- Use `SEED=42` for reproducibility
- `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard baseline integrity
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Do not re-pin golden baselines to silence drift — see ledger open items (E041, E042)

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Decide on verification level (quick/extended/full) based on goal