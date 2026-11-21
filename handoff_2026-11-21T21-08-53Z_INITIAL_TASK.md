# Agentic Work Session Handoff

**Timestamp**: 2026-11-21T21:08:53Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State

- **Research Phase**: Complete (E001–E043)
- **Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Current Focus**: Verification/reproducibility of surviving strategies
- **Working tree**: clean at handoff time (no golden-artifact drift)

## Quick Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Recover the golden artifacts after an interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Integrity Notes

1. **Golden files** in `experiments/*.json` are canonical artifacts — the verification suite overwrites them while re-running drivers and restores them afterwards. Never leave a run half-finished; recover with `--restore-only`.
2. **Golden baseline** is pinned in `ledger/golden_baseline.json` (SHA-256). Never re-pin as a side effect of verification — the committed golden is the authoritative record, not the latest re-run.
3. **Seed 42** is mandatory for all runs (walk-forward + placebo RNG).
4. **Data cache** in `data/` is gitignored except pinned vintages 2026-10-11 and 2026-10-12. Cache coverage is enforced by `scripts/check_data_coverage.py` + `ledger/data_baseline.json`.
5. **E029 fundamentals** are pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` — fully offline-reproducible.
6. **Optimizer determinism**: the tangency QP in `src/portfolio_opt.py` is ill-conditioned (1-ulp sensitivity); the solver-status gating defect is fixed (pinned by `tests/test_portfolio_opt.py`). Do **not** re-pin E041/E042 to silence drift.

## Open Items (from ledger)

- **E041**: 133 numeric differences remain (ill-conditioned QP; optimizer fault fixed, 3 structural diffs eliminated). Decision unchanged: REJECTED 3/5.
- **E042**: grid artifacts drift by 29–133 differences (same root cause). Decision unchanged: PARTIAL.
- See `ledger/RESEARCH_LEDGER.md` entries E045, E048, E049 for details.

## Initial Task for Next Session

Run `SEED=42 bash scripts/check.sh` first to confirm environment/golden integrity, then `SEED=42 python3 run_all_verification.py` to confirm the surviving strategies still reproduce. Review any drift in the extended drivers, and consult the open items above before promoting any strategy. Do **not** modify or re-pin golden artifacts; if a verification run is interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only`.

(End of file)