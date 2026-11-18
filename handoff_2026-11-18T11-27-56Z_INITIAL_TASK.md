# Agentic Work Session Handoff

**Timestamp:** 2026-11-18T11:27:56Z
**Session ID:** Initial handoff for next agentic session
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes for Next Session

1. **Golden artifacts**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them during re-run and restores afterward. Never leave a verification run half-finished.

2. **Baseline integrity**:
   - Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker
   - `scripts/check_goldens_clean.py` compares working tree with HEAD
   - `scripts/check_golden_baseline.py` compares with SHA-256 in `ledger/golden_baseline.json`
   - Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Reproducibility**: Always use `SEED=42`. Cache coverage is enforced - all data inputs must be pinned in `ledger/data_baseline.json`.

4. **Known drift**:
   - E011, E030, E041 show small numeric drift (1-ulp sensitivity)
   - E029 is now offline-reproducible (fundamentals pinned in `data/fundamentals/`)
   - E041's optimizer defect is fixed but 133 numeric differences remain (ill-conditioned QP)

5. **Optimizer determinism**: `src/portfolio_opt.py` validates on problem constraints, not solver exit status. Tangency QP remains ill-conditioned.

## Current State

- Research phase complete (E001–E043)
- Ledger documents surviving validated strategies
- Verification suite passes with known drift allowances
- No active experiment drivers running

## Suggested Next Steps

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Review `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Consider E042 confirmatory run with full placebo if pursuing min-var strategy
4. Address open items in ledger (E041/E042 re-pinning decision)
