# Agentic Work Session Handoff

**Timestamp**: 2026-11-18T18:22:16Z
**Session**: Initial task message for next agentic work session

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands
- `SEED=42 bash scripts/check.sh` — Fast convention-robustness check + template validation
- `SEED=42 python3 run_all_verification.py` — Quick full verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — Extended verification (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — Full verification (~15 min)
- `SEED=42 python3 run_all_verification.py --restore-only` — Recover golden artifacts

## Baseline Integrity
- `experiments/*.json` are canonical research artifacts
- Verification suite overwrites them during re-run and restores afterward
- Backup in `.verify_snapshot/` with `ACTIVE.json` marker
- `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard integrity
- **Never commit verification output** — restore before committing

## Reproducibility
- Seed: Always `SEED=42` (walk-forward + placebo RNG)
- Convention: Close-to-close v1.2.3 primary, overnight decomposition reported alongside
- Data: Cached parquet in `data/` (gitignored except pinned vintages)
- Cache coverage enforced via `scripts/check_data_coverage.py`

## Current State
- No active verification run
- Working tree clean (no uncommitted changes to experiments/)
- Ready for next task

## Next Steps (suggested)
1. Run `make check` to verify baseline integrity
2. Run `make verify-quick` for quick full verification
3. Or run specific experiment drivers as needed

---
*This handoff was created automatically at session start.*