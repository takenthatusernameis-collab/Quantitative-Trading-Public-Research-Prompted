# Agentic Work Session Handoff

**Timestamp**: 2026-11-20T06:30:56Z
**Session ID**: Initial handoff for next session
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Project Context

This is a quantitative trading research repository covering 2014–2026 US equities, futures, and macro data. Research phase is complete (experiments E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands (from AGENTS.md)

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

## Important Notes

- **Golden files**: `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores them afterward.
- **Seed**: Always use `SEED=42` for reproducibility.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages).
- **Cache coverage**: Enforced invariant - all `data.download()` call sites must have committed cache files matching SHA-256 in `ledger/data_baseline.json`.
- **Optimizer determinacy**: `src/portfolio_opt.py` validates solver answers on problem constraints, not solver exit status (ledger E049).
- **E029**: Offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/`).
- **E030**: Reproduces with 0 differences since 2026-10-20 (16-ETF panel committed).

## Baseline Integrity

- Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker (pid-based ownership)
- `scripts/check_goldens_clean.py` fails when tracked artifacts differ from HEAD
- `scripts/check_golden_baseline.py` compares artifacts with SHA-256 in `ledger/golden_baseline.json`
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Review any open items in the ledger (E041/E042 optimizer drift, E049 optimizer determinism)
4. Consider running verification suite if making changes