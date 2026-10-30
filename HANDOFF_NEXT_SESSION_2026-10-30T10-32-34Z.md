# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-30T10-32-34Z (UTC)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `021c47b`
**Working tree:** 12 uncommitted changes
**Snapshot state:** `.verify_snapshot/` does NOT exist

This session only created this durable handoff. No source changes were made and no verification run was executed.

## Initial Task (Start Here)

**Task:** Baseline integrity first. Run `SEED=42 bash scripts/check.sh` and verify repo is clean. If checks pass, proceed to the standing E049 follow-up (tangency QP ill-conditioning) to make E041/E042 grid artifacts reproduce within tolerance without reintroducing solver-status dependence.

## Concrete Next Steps

1. **Confirm clean baseline:** `SEED=42 bash scripts/check.sh` — expect exit 0.
2. **Confirm tree state:** `git status --short` — clean or only `__pycache__/*.pyc`.
3. **Quick verification:** `SEED=42 python3 run_all_verification.py --skip-slow`.
4. **Investigate well-conditioned solver for small N (<=5 assets):** exact KKT enumeration; CVXOPT/OSQP/custom active-set; preserve feasibility-validation invariant.
5. **Validate:** run E041/E042 offline with `SEED=42 QUANT_RESEARCH_OFFLINE=1`; compare vs goldens.
6. **Document findings:** update `ledger/RESEARCH_LEDGER.md`; re-pin goldens only via `scripts/check_golden_baseline.py --update` with strong rationale.

## Constraints

- Always use `SEED=42`. Use `QUANT_RESEARCH_OFFLINE=1` for verification.
- Never leave `run_all_verification.py` half-finished; recover with `--restore-only`.
- Do not re-pin goldens/baselines to silence drift without ledger justification.
- Do not commit verification outputs; only intentional source/data changes.
- Follow `AGENTS.md`; preserve "judge answer on problem constraints, not solver status".

## Quick Commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --skip-slow
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e041.py
```

## Key Files
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`
- `ledger/RESEARCH_LEDGER.md`
- `scripts/check*.py`, `run_all_verification.py`
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`

(End of file)