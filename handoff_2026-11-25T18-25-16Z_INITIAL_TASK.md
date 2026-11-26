# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T06:05:47Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates.

**Research Phase**: Complete (E001–E043)
**Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`

---

## Key Verification Commands

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

---

## Critical Baseline Integrity Rules

1. **`experiments/*.json` are canonical research artifacts** — verification suite overwrites them during re-run and restores afterward
2. **Never leave a verification run half-finished** — use `--restore-only` to recover if interrupted
3. **Golden baseline pinned in `ledger/golden_baseline.json`** — do not re-pin without ledger entry
4. **Cache coverage is enforced invariant** — `scripts/check_data_coverage.py` validates all data inputs

---

## Recent Key Findings (from ledger)

- **E050 fix** (commit `72dc947`): Exact KKT active-set enumeration as primary tangency solver → bit-reproducible artifacts
- **E029**: Offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/`)
- **E030**: Reproduces with 0 differences since 2026-10-20 (16-ETF panel committed)
- **E041/E042**: Optimizer determinism fixed — no remaining tolerance violations

---

## Next Session Starting Points

1. **Run quick verification** to confirm current state: `SEED=42 make verify-quick`
2. **Check golden baseline integrity**: `SEED=42 python3 scripts/check_golden_baseline.py`
3. **Review ledger** for any pending confirmatory runs: `cat ledger/RESEARCH_LEDGER.md`
4. **Consider extended/full verification** if time permits

---

## Environment

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Dependencies**: `pip install -r requirements.txt`
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Offline mode**: Set `QUANT_RESEARCH_OFFLINE=1` for verification runs

---

*This handoff was created automatically at session start. Update as work progresses.*