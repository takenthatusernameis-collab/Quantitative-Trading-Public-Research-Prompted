# Agent Handoff — 2026-11-16T09:34:23Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043); surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working dir**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Incoming task**: Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.

## Key Commands (from AGENTS.md)
```bash
# Fast convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh
# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# Full verification (~15 min, n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full
# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

## Critical Baseline Integrity Notes
- `experiments/*.json` are canonical artifacts — verification overwrites & restores them
- **Never leave a verification run half-finished** (stale `.verify_snapshot/` with `ACTIVE.json` pid marker)
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` (SHA-256); `check_golden_baseline.py` guards against silent replacement
- Data cache coverage enforced via `scripts/check_data_coverage.py` → `ledger/data_baseline.json`

## Known Drift / Open Items (per ledger)
- **E041**: 133 numeric differences (1-ulp ill-conditioned QP); 3 structural diffs fixed. **Do not re-pin**.
- **E042** grid artifacts drift 29–133 diffs (same optimizer issue). **Do not re-pin**.
- **E030**: Offline-reproducible (pinned 16-ETF panel in `data/`); golden re-pinned 2026-10-20.
- **E029**: Offline-reproducible (fundamentals pinned in `data/fundamentals/` per `fundamentals_vintages.json`).

## Reproducibility Requirements
- Always `SEED=42` (walk-forward + placebo RNG)
- `QUANT_RESEARCH_OFFLINE=1` for verification (fails on missing cache)
- Dependencies: `pip install -r requirements.txt` (cvxpy/cvxopt optional)

## Next Steps / Suggested Work
1. Run `SEED=42 bash scripts/check.sh` to verify baseline health before any changes
2. If modifying experiments, ensure pre-registration blocks and falsification expectations are documented
3. Any new data inputs: commit cache file + `python3 scripts/check_data_coverage.py --update`
4. Do not commit verification output — restore goldens first (`--restore-only`)

## Files to Review
- `ledger/RESEARCH_LEDGER.md` — validated strategies & dispositions
- `ledger/golden_baseline.json` — pinned artifact fingerprints
- `ledger/data_baseline.json` — pinned data cache fingerprints
- `scripts/check_golden_baseline.py` — baseline integrity guard
- `src/portfolio_opt.py` — optimizer (determinism rule pinned by `tests/test_portfolio_opt.py`)
