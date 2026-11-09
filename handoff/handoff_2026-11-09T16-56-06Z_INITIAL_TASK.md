# Handoff — 2026-11-09T17:08:40Z

## Session Context
- **Project**: Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Quick Commands
```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Restore golden artifacts after interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Conventions
- **Seed**: Always `SEED=42`
- **Golden files**: `experiments/*.json` are canonical — never commit verification output
- **Data**: Cached parquet in `data/` (pinned vintages 2026-10-11, 2026-10-12)
- **Offline mode**: `QUANT_RESEARCH_OFFLINE=1` enforced during verification
- **Pre-registration**: All experiments have `pre_registered` blocks; goalposts never moved post-hoc

## Critical Notes
- Verification suite backs up goldens to `.verify_snapshot/` with `ACTIVE.json` marker (pid-locked)
- If `scripts/check.sh` reports golden mismatch, fix **before** committing
- `scripts/check_golden_baseline.py` compares artifacts to SHA-256 in `ledger/golden_baseline.json`
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- Cache coverage enforced via `scripts/check_data_coverage.py` → `ledger/data_baseline.json`

## Open Items (from ledger)
- E041: 133 numeric diffs remain (ill-conditioned QP, 1-ulp sensitivity) — do not re-pin
- E030: Now reproduces with 0 diffs (panel committed, golden re-pinned per ledger E048)
- E029: Offline-reproducible since 2026-10-20 (ledger E045)

## Next Steps
- Run `SEED=42 python3 run_all_verification.py --extended` to validate extended driver set
- Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and promotion gates
- Review `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` after extended run (gitignored)