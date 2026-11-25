# Agentic Work Session Handoff

**Timestamp:** 2026-11-25T08:09:51Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status

**Research Phase:** Complete (E001–E043)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

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

## Critical Notes for Next Session

1. **Baseline Integrity:** `experiments/*.json` are canonical research artifacts. Verification suite overwrites them during re-run and restores afterward. Never leave a verification run half-finished.

2. **Recovery:** If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Golden Baseline:** `ledger/golden_baseline.json` pins SHA-256 fingerprints. Replacing an artifact requires re-pinning via `python3 scripts/check_golden_baseline.py --update`

4. **Data Coverage:** Cache coverage is an enforced invariant. `scripts/check_data_coverage.py` validates all cache files exist, are git-tracked, and match SHA-256 in `ledger/data_baseline.json`

5. **Reproducibility:** Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.

## Key Files to Reference

- `AGENTS.md` - Project commands & conventions
- `ledger/RESEARCH_LEDGER.md` - Validated strategies documentation
- `ledger/golden_baseline.json` - SHA-256 pinned artifacts
- `ledger/data_baseline.json` - SHA-256 pinned data files
- `data/vintages.json` - Pinned data vintage (2026-10-12)
- `data/fundamentals_vintages.json` - E029 fundamentals snapshot

## Pending/Next Steps

- [ ] No explicit pending tasks from current session
- [ ] Verify all experiment artifacts are at baseline (run `make check`)
- [ ] Consider running verification suite if changes were made

---

*This handoff was created automatically at session start. Update as work progresses.*