# Agentic Work Session Handoff

**Timestamp**: 2026-11-14T08:18:51Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Verification Commands (from AGENTS.md)

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

## Key Integrity Notes

- **Golden files**: `experiments/*.json` are canonical artifacts. Verification suite backs them up before re-running and restores afterward.
- **Never leave verification half-finished**: If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` to recover.
- **Baseline pinned in**: `ledger/golden_baseline.json` (SHA-256 fingerprints)
- **Data cache**: Pinned vintages in `data/vintages.json` (2026-10-12) and `data/fundamentals_vintages.json` (E029 fundamentals)
- **Seed**: Always use `SEED=42` for reproducibility

## Current State

No active verification run detected. Working tree is clean relative to HEAD for `experiments/*.json` artifacts.

---

*Next session: Check `scripts/check.sh` first to verify baseline integrity before any verification run.*