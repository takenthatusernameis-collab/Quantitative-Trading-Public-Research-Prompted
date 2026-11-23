# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T15:21:23Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State
- **Research phase**: Complete (E001–E043)
- **Validated strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Verification suite**: Ready for reproduction/verification

## Quick Commands
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min + 96-config grid)
SEED=42 python3 run_all_verification.py --full
```

## Key Files
- `AGENTS.md` — Project commands & conventions
- `ledger/RESEARCH_LEDGER.md` — Surviving validated strategies
- `experiments/*.json` — Canonical golden artifacts (git-tracked)
- `data/vintages.json` — Pinned data cache (2026-10-12)
- `data/fundamentals_vintages.json` — Pinned fundamentals for E029

## Important Notes
- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Golden baseline**: Pinned in `ledger/golden_baseline.json` (SHA-256 fingerprints)
- **Data coverage**: Enforced invariant — all `data.download()` calls must have committed cache entries
- **Seed**: Always use `SEED=42` for reproducibility

## Next Steps
- Run `SEED=42 bash scripts/check.sh` to verify environment
- Choose verification tier based on time budget
- Any code changes require re-running verification to update goldens (with ledger entry)

---
*This handoff was created automatically at session start.*