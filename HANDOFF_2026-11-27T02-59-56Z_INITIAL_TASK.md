# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T04:02:04Z
**Session**: Initial task message for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Integrity Notes (READ BEFORE RUNNING)
- `experiments/*.json` are canonical research artifacts
- Verification suite overwrites them while re-running and restores afterward
- **Never leave a verification run half-finished** — baseline will be corrupted
- Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker (pid)
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against silent baseline replacement

## Reproducibility Requirements
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Convention**: Close-to-close is v1.2.3 primary; overnight decomposition reported alongside
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Cache coverage enforced**: `scripts/check_data_coverage.py` validates every download call site
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current experiment status
3. Decide on verification level: `make check` → `make verify-quick` → `make verify-extended` → `make verify-full`
4. Any new experiments must follow pre-registration protocol with falsification expectations

---
*This handoff was created automatically at session start to ensure durable context transfer.*