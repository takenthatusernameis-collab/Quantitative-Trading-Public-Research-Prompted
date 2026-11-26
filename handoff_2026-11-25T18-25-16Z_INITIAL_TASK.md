# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T05:08:41Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Key Context

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores them afterward.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`.
- **Baseline Integrity**: Verification runs must never be left half-finished. Use `--restore-only` to recover golden artifacts after interrupted runs.
- **CI Gate**: Template at `.github/workflow-templates/verification-gate.yml` — maintainer must create actual workflow via GitHub UI.

## Next Session Guidance

1. Run `SEED=42 bash scripts/check.sh` first to verify baseline integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Use `make verify-quick` for standard verification
4. Never commit verification output — restore goldens with `--restore-only` if interrupted

---
*This handoff was created automatically at session start.*