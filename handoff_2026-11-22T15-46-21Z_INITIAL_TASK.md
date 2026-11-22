# Handoff — Agentic Work Session

**Timestamp:** 2026-11-22T15:47:27Z
**Session ID:** (auto-generated)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands (from AGENTS.md)
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

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
#   or
make verify
```

## Critical Baseline Integrity Notes
- `experiments/*.json` are canonical research artifacts
- Verification suite overwrites them while re-running drivers and restores them afterwards
- **A verification run must never be left half-finished**
- Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker holding owning pid
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` — never re-pin as side effect of verification

## Key Files to Understand
- `AGENTS.md` — Project commands & conventions (this file's source)
- `ledger/RESEARCH_LEDGER.md` — Surviving validated strategies
- `ledger/golden_baseline.json` — SHA-256 fingerprints of canonical artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of pinned data
- `scripts/check.sh` — Fast convention-robustness + golden baseline checks
- `scripts/check_goldens_clean.py` — Compares working tree with HEAD
- `scripts/check_golden_baseline.py` — Compares tracked artifacts with pinned SHA-256
- `scripts/check_data_coverage.py` — Enforces cache coverage invariant

## Reproducibility Requirements
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Offline mode**: Verification runs with `QUANT_RESEARCH_OFFLINE=1`
- **E029 fundamentals**: Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

## Open Items / Known Drift (from AGENTS.md)
- **E041**: 133 numeric differences (1-ulp sensitivity of ill-conditioned QP) — do NOT re-pin
- **E030**: Reproduces with 0 differences since 2026-10-20 (ledger E048)
- **E029**: Offline-reproducible since 2026-10-20 (ledger E045)
- **Optimizer determinism**: `src/portfolio_opt.py` validates on problem constraints, not solver exit status (pinned by `tests/test_portfolio_opt.py`)

## Next Session Suggested Starting Points
1. Run `make check` to verify baseline integrity before any work
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Review any open items in the ledger (E041, E049, etc.)
4. Consider running `make verify-quick` if baseline is clean

---
*This handoff was created automatically at session start. Update as needed during work.*