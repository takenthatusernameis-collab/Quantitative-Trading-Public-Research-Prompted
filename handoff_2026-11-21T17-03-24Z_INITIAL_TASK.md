# Agentic Work Session Handoff

**Timestamp:** 2026-11-21T17:05:14Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Notes for Next Session

- **Golden artifacts**: `experiments/*.json` are canonical. Verification suite overwrites and restores them — never leave a verification run half-finished.
- **Recovery**: If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Seed**: Always use `SEED=42` for reproducibility
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals pinned in `data/fundamentals/`
- **CI Gate**: Template at `.github/workflow-templates/verification-gate.yml` — maintainer must create actual workflow via GitHub UI
- **Lint/Format**: `python3 -m py_compile` on changed files

## Baseline Integrity Reminders

1. `scripts/check_goldens_clean.py` compares working tree with HEAD
2. `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 in `ledger/golden_baseline.json`
3. `scripts/check_data_coverage.py` enforces cache coverage — all `data.download()` call sites must have pinned cache files
4. Never re-pin artifacts as side effect of verification — committed golden is authoritative

## Open Items (from ledger)

- E041 optimizer drift: 133 numeric differences remain (ill-conditioned QP, 1-ulp sensitivity) — do not re-pin
- E042 grid artifacts drift by 29-133 differences — do not re-pin
- E029 offline-reproducible since 2026-10-20 (fundamentals pinned)
- E030 offline-reproducible since 2026-10-20 (16-ETF panel committed)

---

*This handoff was created automatically at session start. Update as work progresses.*