# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T12:59:00Z
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

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Critical Integrity Notes

1. **Golden Files**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them during re-run and restores afterward. **Never leave a verification run half-finished**.

2. **Recovery**: If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Baseline Protection**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` (both in `scripts/check.sh`) guard against:
   - Working tree vs HEAD drift
   - Committed artifacts vs pinned SHA-256 in `ledger/golden_baseline.json` drift

4. **Data Cache**: Cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`.

5. **Offline Reproducibility**: Set `QUANT_RESEARCH_OFFLINE=1` to fail hard on missing cache instead of silent download.

## Recent Ledger Entries (Key Fixes)

- **E049**: Optimizer determinism fix — SLSQP status-gating removed, validation on constraints not exit status
- **E050**: Exact KKT active-set enumeration as primary tangency solver — closed E041/E042 drift, artifacts now bit-reproducible
- **E048**: Cache coverage enforced — E030 16-ETF panel committed, E029 fundamentals snapshot pinned
- **E045**: E029 offline-reproducible since 2026-10-20

## Do Not Re-pin

Per ledger E050 precedent: **Do not re-pin E041/E042 to "silence" tolerance violations** — there are none remaining. Re-pinning only warranted for *deliberate* code changes altering published numbers, recorded in ledger first.

## Next Session Suggested Starting Points

- Run `make check` to verify current state
- Run `make verify-quick` for full reproduction check
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
- Check `experiments/` for current golden artifacts

---

*This handoff was created automatically at session initialization. Update as work progresses.*