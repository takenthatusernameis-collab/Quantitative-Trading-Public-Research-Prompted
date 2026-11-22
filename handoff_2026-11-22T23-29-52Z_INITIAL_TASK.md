# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-22T23:29:52Z
**Session ID**: Initial handoff created by user request
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 experiment drivers)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 committed drivers)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Important Notes

- **Seed**: Always use `SEED=42` for walk-forward + placebo RNG reproducibility.
- **Golden files**: `experiments/*.json` are committed artifacts — never commit verification output. Verification backs them up and restores them afterwards.
- **Recovery**: If verification is interrupted (SIGKILL/OOM/timeout), run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is enforced by `scripts/check_data_coverage.py`; missing cache entries fail hard offline. `QUANT_RESEARCH_OFFLINE=1` is used by the verification suite.
- **Optimizer determinism**: `src/portfolio_opt.py` validates solver answers on problem constraints, never exit status. E041/E042 grid artifacts drift by 29–133 numeric diffs (ill-conditioned QP); do not re-pin to silence.

## Open Items (from ledger)

- E041 optimizer drift: 133 numeric differences remain (1-ulp sensitivity of ill-conditioned QP); decision/gates unchanged (REJECTED 3/5).
- CI workflow cannot be created by agents — template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create it via the GitHub UI.

## Current State

- Research phase: COMPLETE (E001–E043)
- Verification suite: Operational (quick / extended / full modes)
- Baseline integrity: Protected by `check_goldens_clean.py` and `check_golden_baseline.py`
- No active verification run (check `scripts/check_goldens_clean.py` for stale snapshots)

## Initial Task for Next Session

Run `SEED=42 bash scripts/check.sh` to confirm a clean baseline state. If clean, proceed with `make verify-quick` (~8 min). Review `ledger/RESEARCH_LEDGER.md` for open items before any re-pinning of goldens or data.
