# Agentic Work Session Handoff

**Timestamp**: 2026-11-16T18:58:05Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

**Research Phase**: COMPLETE (E001–E043 executed)
**Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`

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

## Key Integrity Notes

1. **Golden Files**: `experiments/*.json` are canonical artifacts. Verification suite backs them up to `.verify_snapshot/` and restores after.
2. **Never leave verification half-finished** - use `--restore-only` to recover if interrupted.
3. **Baseline Integrity**: `scripts/check_golden_baseline.py` compares artifacts to SHA-256 in `ledger/golden_baseline.json`. Re-pinning requires explicit `--update`.
4. **Data Cache**: Pinned vintages in `data/vintages.json` (2026-10-12) and `data/fundamentals_vintages.json` (E029). Cache coverage enforced by `scripts/check_data_coverage.py`.
5. **Reproducibility**: Always use `SEED=42`. Close-to-close is primary convention v1.2.3.

## Known Drift Items (from ledger)

- **E041**: 133 numeric differences (1-ulp sensitivity of ill-conditioned QP) - do NOT re-pin
- **E042**: Grid artifacts drift by 29-133 differences - do NOT re-pin
- **E030**: Now 0 differences since 2026-10-20 (panel committed)
- **E029**: Now 0 differences since 2026-10-20 (fundamentals pinned)

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Review any open items in ledger (E041 optimizer determinism, E042 grid drift)
4. Consider running `verify-quick` for fast validation before making changes

## Important Files

- `AGENTS.md` - Project commands & conventions (this file's source)
- `ledger/RESEARCH_LEDGER.md` - Validated strategies & dispositions
- `ledger/golden_baseline.json` - SHA-256 fingerprints of canonical artifacts
- `ledger/data_baseline.json` - SHA-256 fingerprints of pinned data caches
- `scripts/check.sh` - Fast convention-robustness check
- `run_all_verification.py` - Full verification suite