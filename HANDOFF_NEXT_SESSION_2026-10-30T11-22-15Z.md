# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-30T11:25:30Z (UTC)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**Snapshot state:** `.verify_snapshot/` does NOT exist

This session created/updated this durable handoff. No source changes were made and no verification run was executed.

## INITIAL TASK (START HERE)

**PRIORITY 1 - Baseline integrity:** Run `SEED=42 bash scripts/check.sh` and confirm repo is clean. All checks must pass before proceeding.

**PRIORITY 2 - E049 follow-up (if checks pass):** Investigate and fix tangency QP ill-conditioning causing E041/E042 grid artifacts to drift. Goal: make E041/E042 reproduce within tolerance WITHOUT reintroducing solver-status dependence (preserve "judge answer on problem constraints, not solver status" invariant). Do NOT re-pin goldens to silence drift without ledger justification.

## Concrete Next Steps

1. **Confirm clean baseline:** `SEED=42 bash scripts/check.sh` — expect exit 0. If it fails, restore from git if needed.
2. **Confirm tree state:** `git status --short` — clean or only `__pycache__/*.pyc`.
3. **Quick verification (optional):** `SEED=42 python3 run_all_verification.py --skip-slow` to see current state.
4. **Investigate well-conditioned solver for small N (<=5 assets):** Try exact KKT enumeration; consider CVXOPT/OSQP/custom active-set approaches. Must preserve feasibility-validation invariant (validate solver answer on problem constraints, never solver exit status).
5. **Test fix:** Run E041/E042 offline with `SEED=42 QUANT_RESEARCH_OFFLINE=1` and compare vs committed goldens.
6. **Document:** Update `ledger/RESEARCH_LEDGER.md` with findings. Only re-pin goldens/baselines via `scripts/check_golden_baseline.py --update` with strong rationale.

## Constraints

- Always use `SEED=42`. Use `QUANT_RESEARCH_OFFLINE=1` for verification.
- Never leave `run_all_verification.py` half-finished; recover with `--restore-only`.
- Do not re-pin goldens/baselines to silence drift without ledger justification.
- Do not commit verification outputs; only intentional source/data changes.
- Follow `AGENTS.md`; preserve "judge answer on problem constraints, not solver status" invariant.

## Quick Commands
```bash
SEED=42 bash scripts/check.sh
git status --short
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e041.py
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e042.py --n-sim 50
```

## Key Files
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`
- `ledger/RESEARCH_LEDGER.md` (E049)
- `experiments/run_e041.py`, `experiments/run_e042.py`
