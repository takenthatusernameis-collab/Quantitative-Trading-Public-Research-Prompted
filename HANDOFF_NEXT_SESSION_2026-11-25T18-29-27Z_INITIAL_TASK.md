# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T18:29:27Z
**Session ID**: Handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Git State

- Branch: `main`
- Working tree: clean (`git status` reported no changes)
- Last commit: `01f908a0 chore(kilo): checkpoint agent session`

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Recover golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Individual Experiment Commands

```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Critical Notes

1. **Golden files**: `experiments/*.json` are committed canonical artifacts. Verification suite backs them up before re-running and restores afterward — the baseline is never modified by verification.
2. **Baseline integrity**: If `scripts/check.sh` reports a golden mismatch, fix it **before** committing. A checkpoint commit that captures verification output silently replaces the canonical baseline.
3. **Reproducibility**: Always use `SEED=42` (walk-forward + placebo RNG).
4. **Data**: Cached parquet in `data/` (gitignored except pinned vintages). E029's fundamentals are separately pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`.
5. **Optimizer determinism**: `src/portfolio_opt.py` validates on problem constraints, not solver exit status (ledger E049/E050).
6. **Do not commit verification output**: If a run is interrupted, restore before committing (`run_all_verification.py --restore-only`).
7. **Cache coverage invariant**: Every `data.download()` call site requires a committed, SHA-256-pinned cache file (checked by `scripts/check_data_coverage.py`).

## Current State

- Research phase: Complete (E001–E043)
- Ledger: `ledger/RESEARCH_LEDGER.md` contains surviving validated strategies
- Verification: Ready to run with `SEED=42` prefix
- CI workflow cannot be created by agents — template at `.github/workflow-templates/verification-gate.yml`

## Initial Task for Next Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment cleanliness.
2. Run `SEED=42 python3 run_all_verification.py --extended` to reproduce committed drivers and compare against goldens (`numeric_tol=1e-4`); report any drift, do NOT re-pin goldens.
3. Await explicit user instructions for new experiments; any new experiment must follow the pre-registration protocol.

---

*This handoff was created at 2026-11-25T18:29:27Z. Update as needed during work.*
