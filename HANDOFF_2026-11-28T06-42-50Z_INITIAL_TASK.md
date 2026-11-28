# Agent Handoff — 2026-11-28T08:36:37Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Git Status**: Clean (no uncommitted changes expected)

## Key Commands for Next Session
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
```

## Critical Baseline Integrity Notes
- `experiments/*.json` are canonical research artifacts — verification suite overwrites and restores them
- **Never leave a verification run half-finished** — use `--restore-only` to recover if interrupted
- Golden baseline pinned in `ledger/golden_baseline.json` (SHA-256 fingerprints)
- Data cache coverage enforced via `scripts/check_data_coverage.py` — all downloads must be pinned
- Optimizer determinacy fixed in E050 (exact KKT active-set enumeration)

## Current State
- No active verification run (snapshot directory `.verify_snapshot/` should be clean)
- All 18 extended drivers reproduce with 0 differences (measured 2026-11-23T05:17Z)
- E029 fundamentals pinned offline in `data/fundamentals/` per `data/fundamentals_vintages.json`
- E030 16-ETF panel committed and golden re-pinned

## Pending / Next Steps
- [ ] Run `make check` to verify baseline integrity before any new work
- [ ] If adding new experiments: pre-register with falsification expectations and sensitivity grid
- [ ] Any new data inputs: commit cache file and re-pin with `check_data_coverage.py --update`

## Reproducibility Requirements
- Always use `SEED=42` (walk-forward + placebo RNG)
- Convention: Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- Dependencies: `pip install -r requirements.txt` (cvxpy/cvxopt optional)

## Important Files to Reference
- `AGENTS.md` — Project commands & conventions (this file's source)
- `ledger/RESEARCH_LEDGER.md` — Validated strategies and dispositions
- `ledger/golden_baseline.json` — SHA-256 pinned artifact fingerprints
- `data/vintages.json` — Pinned data cache vintages
- `scripts/check.sh` — Fast convention-robustness check (run first)