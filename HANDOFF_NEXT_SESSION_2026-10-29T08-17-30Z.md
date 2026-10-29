# Handoff for Next Agentic Work Session

**Created:** 2026-10-29T08:17:30Z
**From:** Current session (Kilo)
**To:** Next agentic work session
**Status:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Verification infrastructure hardened (golden baselines pinned, cache coverage enforced, optimizer determinism fixed).

## INITIAL TASK (Start Here)

**Maintain baseline integrity; investigate and address the remaining numeric drift in E041/E042 from ill-conditioned QP (optimizer determinism).**

This is the only known open verification issue. All other guards pass. Do **not** re-pin goldens to silence QP conditioning drift without strong justification.

### Current State (verified at handoff time, 2026-10-29T08:17Z)
- Working tree clean except cached `.pyc` files (gitignored, irrelevant). No live `.verify_snapshot/` — no interrupted verification run pending.
- `SEED=42 bash scripts/check.sh` → **ALL CHECKS PASSED** (JSON artifacts, json guard, golden cleanliness, golden baseline, data coverage, experiment imports, unit tests, template validation, convention robustness).
- Quick verification: passes (8 drivers: E012, E023, E024--merge, E027, E035, E037, E039, E042-lead).
- Extended verification: drifts on **E041 (133 numeric differences)** and **E042 (29 numeric differences)** due to 1-ulp sensitivity of ill-conditioned tangency/min-var QP.
- Optimizer fix applied (E049): `src/portfolio_opt.py` now validates constraints (not solver exit status). `tests/test_portfolio_opt.py` added as first-class guard.
- Golden baseline pinned in `ledger/golden_baseline.json` — never re-pin as side effect of verification.
- Data coverage enforced via `ledger/data_baseline.json` (all driver inputs pinned/cached).

### What to do first (concrete)
1. **Read context**: `ledger/RESEARCH_LEDGER.md` (E049) and `src/portfolio_opt.py` + `tests/test_portfolio_opt.py`.
2. **Confirm drift state**: `SEED=42 python3 run_all_verification.py --extended` (observe E041/E042 diff counts).
3. **Understand conditioning**: Look at how tangency/min-var QP is formulated in `src/portfolio_opt.py` and where E041/E042 build the optimization problem (drivers `experiments/run_e041.py`, `experiments/run_e042.py`).
4. **Explore numerical fixes** (without changing economic results): scaling/regularization, better conditioning, solver options, or formulation changes that preserve feasibility/optimality to within acceptable precision. Any change must keep constraint validation passing.
5. **Verify**: Run `SEED=42 bash scripts/check.sh` and `SEED=42 python3 run_all_verification.py --extended`. If drift reduces below tolerance or becomes explainable with justification, only then consider updating tolerances with explicit ledger entry — **do not** re-pin goldens.
6. **Document**: Update `ledger/RESEARCH_LEDGER.md` with findings/changes.

### Deferred (only after stability work is clean)
- **Blend optimization** (E015 TSM+DN weight optimization). Only after (1)-(2) stable and clean verification passes. If pursued, pre-register gates/sensitivity, use `SEED=42`, follow cost model, and never touch goldens.

## Quick Commands
```bash
# Fast integrity check
SEED=42 bash scripts/check.sh

# Quick/full verification (restores goldens after)
SEED=42 python3 run_all_verification.py        # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full

# Recover if left half-finished
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Files
- `ledger/RESEARCH_LEDGER.md` (E049)
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`
- `experiments/run_e041.py`, `experiments/run_e042.py`
- `experiments/e041_*.json`, `experiments/e042_*.json`
- `run_all_verification.py`, `scripts/check.sh`
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints

## Guardrails
- Always use `SEED=42`
- Never re-pin goldens to silence numeric drift from ill-conditioned QP without strong justification
- Never modify `experiments/*.json` golden files without explicit justification + `--update`
- Follow offline discipline (`QUANT_RESEARCH_OFFLINE=1` in verification)
- Pre-register any new experiment before running; no goalpost moving
- Cost model: tc=0.5bps + slippage=0.2bps, next-day open execution

(End of file)