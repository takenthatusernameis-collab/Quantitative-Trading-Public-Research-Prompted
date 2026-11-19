# Agentic Work Session Handoff

**Timestamp**: 2026-11-19T19:06:12Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

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

## Important Notes

- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores afterward.
- **Do not commit verification output**: If a run is interrupted, restore with `run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Cache coverage is enforced**: `scripts/check_data_coverage.py` validates all data inputs are pinned
- **Optimizer determinicity**: `src/portfolio_opt.py` validates solver answers on constraints, not exit status (see ledger E049)
- **Do not leave verification runs half-finished**: snapshot is repo-local `.verify_snapshot/` with `ACTIVE.json`

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Review any open items in the ledger (e.g., E041 drift, E042/E041 grid artifacts)
4. Consider running verification suite to validate current state

## Files to Reference

- `AGENTS.md` - Project commands & conventions
- `ledger/RESEARCH_LEDGER.md` - Validated strategies and dispositions
- `ledger/golden_baseline.json` - SHA-256 fingerprints for golden artifacts
- `ledger/data_baseline.json` - SHA-256 fingerprints for data cache
- `scripts/check.sh` - Fast convention-robustness check
- `run_all_verification.py` - Full verification suite

(End of file)
" filePath="/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/handoff_2026-11-19T19-06-12Z_INITIAL_TASK.md"