# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T13:02:54Z
**Session ID**: Initial handoff created at session start
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

**Research Phase**: COMPLETE (E001–E043)
**Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
**Verification Suite**: Available via `make verify-quick`, `make verify-extended`, `make verify-full`

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 drivers in 5a block)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 committed drivers)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
#   or
make verify
```

## Critical Integrity Notes

1. **Golden Files**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them during re-run and restores afterward. **Never leave a verification run half-finished**.

2. **Recovery**: If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.

3. **Baseline Protection**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` (both in `scripts/check.sh`) guard against working-tree vs HEAD drift and committed artifacts vs pinned SHA-256 in `ledger/golden_baseline.json`.

4. **Data Cache**: Cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`. Set `QUANT_RESEARCH_OFFLINE=1` to fail hard on missing cache instead of silent download.

5. **Do Not Re-pin**: Per ledger E050 precedent, do not re-pin E041/E042 to "silence" tolerance violations — none remain. Re-pinning only warranted for *deliberate* code changes altering published numbers, recorded in ledger first.

## Next Session Suggested Starting Points

- Run `make check` to verify current state
- Run `make verify-quick` for full reproduction check
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
- Check `experiments/` for current golden artifacts

---

*This handoff was created automatically at session initialization. Update as work progresses.*
