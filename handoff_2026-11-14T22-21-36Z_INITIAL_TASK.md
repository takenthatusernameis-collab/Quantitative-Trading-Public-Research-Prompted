# Agentic Work Session Handoff

**Timestamp**: 2026-11-14T22:22:19Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (surviving strategies, rejections, open items)
- **Data cache**: `data/` (gitignored parquet, pinned vintages in `data/vintages.json`, `data/fundamentals_vintages.json`)
- **Golden baseline**: `ledger/golden_baseline.json` (SHA-256 fingerprints of all tracked artifacts)

## Important Notes
- **Never commit verification output** — interrupted runs leave driver output in `experiments/`. Restore with `python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Verification overwrites goldens temporarily** and restores them — never leave a run half-finished
- **Seed**: Always use `SEED=42` for reproducibility
- **Cache coverage enforced**: `scripts/check_data_coverage.py` validates all data inputs are pinned
- **Optimizer determinism**: E041/E042 grid artifacts have known 1-ulp drift (ill-conditioned QP) — do not re-pin to silence

## Next Steps
- Run `make check` to verify convention robustness
- Run `make verify-quick` for full quick verification
- Check `ledger/RESEARCH_LEDGER.md` for open items (E041 optimizer drift, E049 tangency QP ill-conditioning)