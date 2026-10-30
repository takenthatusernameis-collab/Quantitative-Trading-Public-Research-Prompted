# Handoff for Next Agentic Work Session

**Timestamp:** $(date -u +%Y-%m-%dT%H-%M-%SZ) (UTC)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**Working tree:** Clean (no uncommitted changes)

This session created a durable handoff for the next agent. No source changes were made.

## Initial Task (Start Here)

**Task:** Baseline integrity first. Run `SEED=42 bash scripts/check.sh` and verify repo is clean. If checks pass, proceed to the standing E049 follow-up (tangency QP ill-conditioning) to make E041/E042 grid artifacts reproduce within tolerance without reintroducing solver-status dependence.

## Concrete Next Steps

1. **Confirm clean baseline:** `SEED=42 bash scripts/check.sh` — expect exit 0 (py_compile, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `tests/test_portfolio_opt.py`).
2. **Confirm tree state:** `git status --short` — clean.
3. **Quick verification:** `SEED=42 python3 run_all_verification.py --skip-slow` to re-execute the 5a-block drivers.
4. **Investigate well-conditioned solver for small N (<=5 assets):** exact KKT enumeration as reference; CVXOPT/OSQP/custom active-set as stable alternative; preserve feasibility-validation invariant (judge answer on problem constraints, not solver status).
5. **Validate:** run E041/E042 offline with `SEED=42 QUANT_RESEARCH_OFFLINE=1`; compare vs goldens at same tolerances.
6. **Document findings:** update `ledger/RESEARCH_LEDGER.md`; re-pin goldens only via `scripts/check_golden_baseline.py --update` with strong rationale.

## Context

- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Optimizer determinism fix (E049): `src/portfolio_opt.py` validates against constraints not solver status; tests pass.
- Remaining open item: tangency QP ill-conditioned (1-ulp → ~1e-5 moves). E041 (~133 diffs) and E042 (~29 diffs) still drift; not re-pinned.
- E029/E030 offline-reproducible with 0 differences (pinned inputs).

## Constraints

- Always use `SEED=42`. Use `QUANT_RESEARCH_OFFLINE=1` for verification; required caches pinned.
- Never leave `run_all_verification.py` half-finished; recover with `--restore-only` if interrupted.
- Do **not** re-pin goldens/baselines to silence drift without ledger justification.
- Do **not** commit verification outputs; only intentional source/data changes.
- Follow `AGENTS.md`; preserve "judge answer on problem constraints, not solver status".
- No goalpost moves without pre-registered evidence.
- Do **not** commit changes without explicit user direction.

## Quick Commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --skip-slow
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e041.py
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e042_lead.py
```

## Key Files
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`
- `ledger/RESEARCH_LEDGER.md`
- `scripts/check*.py`, `run_all_verification.py`
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`

## Handoff Notes
- This is the durable handoff for the next session. Update symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md` to point here.
