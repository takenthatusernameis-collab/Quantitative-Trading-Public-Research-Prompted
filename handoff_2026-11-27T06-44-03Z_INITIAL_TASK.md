# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T07:47:49Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Notes for Next Session

- **Golden artifacts**: `experiments/*.json` are canonical research artifacts. Verification suite backs them up before re-running and restores them afterward.
- **Seed**: Always use `SEED=42` for reproducibility.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache hit is calendar-independent.
- **Recovery**: If verification is interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Never commit verification output** - restore goldens before committing.

## Recent Context

The verification suite (run_all_verification.py) handles baseline integrity with `.verify_snapshot/` for recovery. The E050 fix (exact KKT active-set enumeration) made E041/E042 artifacts bit-reproducible across environments.

---

*This handoff was created automatically for the next agentic work session.*