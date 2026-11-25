# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T15:21:24Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State

- **Research Phase**: Complete (E001–E043)
- **Surviving Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden Artifacts**: `experiments/*.json` (canonical baselines, pinned SHA-256 in `ledger/golden_baseline.json`)
- **Data**: Cached parquet in `data/` (gitignored except pinned 2026-10-12/2026-10-11 vintages)
- **E029 Fundamentals**: Separately pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

## Key Commands

```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Individual experiments
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e042.py --n-sim 50
```

## Critical Integrity Notes

1. **Verification runs must complete** — they overwrite `experiments/*.json` and restore after. Never leave half-finished.
2. **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Golden baseline pinned in `ledger/golden_baseline.json`** — `scripts/check_golden_baseline.py` enforces this
4. **Cache coverage invariant**: `scripts/check_data_coverage.py` requires all driver data inputs pinned
5. **Do not re-pin artifacts to silence tolerance violations** — only deliberate code changes warrant re-pinning (see E050 precedent)
6. **Optimizer determinism**: SLSQP status-gating removed; exact active-set enumeration (E050 fix) makes E041/E042 bit-reproducible

## Reproducibility Requirements

- **Seed**: Always `SEED=42`
- **Convention**: Close-to-close primary (v1.2.3), overnight decomposition reported alongside
- **Dependencies**: `pip install -r requirements.txt` (cvxpy/cvxopt optional)

## Recent Ledger Entries

- **E048** (2026-10-20): E030 panel committed, golden re-pinned
- **E049** (2026-10-20): Optimizer determinism root-caused, E050 fix landed
- **E050** (2026-11-01): Exact KKT active-set enumeration primary tangency solver; E041/E042 now 0-diff bit-reproducible

## Next Session Suggestions

- Run `make check` to verify baseline integrity
- Run `make verify-quick` for fast verification
- Check `ledger/RESEARCH_LEDGER.md` for surviving strategy documentation
- Review `scripts/check_golden_baseline.py` and `scripts/check_data_coverage.py` for integrity guards

---

*Generated automatically for agentic handoff continuity.*