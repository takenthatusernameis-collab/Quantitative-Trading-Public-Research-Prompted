# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-30T01:39:41Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `94f9d54` (`chore(kilo): checkpoint agent session`)
**Working tree:** clean except `__pycache__/*.pyc` modifications (tracked bytecode caches; no source changes). No `.verify_snapshot/` active. Symlinks `handoff.md`, `handoff_next.md`, `handoff_next_session.md` point here (root).

This session only inspected repository state (git status/diff, AGENTS.md, prior handoff). No source changes were made and no verification run was executed.

## Initial Task (Start Here)

**Task:** Verify repository stability before any new work, then continue the open E049 follow-up item — address tangency QP ill-conditioning so E041/E042 grid artifacts reproduce within tolerance without reintroducing solver-status dependence.

## Context

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Optimizer determinism fix (E049) is in place: `src/portfolio_opt.py` validates answers against problem constraints, not solver `success` status; `tests/test_portfolio_opt.py` passes and is integrated into `scripts/check.sh`.
- Remaining open item: tangency QP is ill-conditioned (1-ulp perturbations move `min_var` answers by ~1e-5). E041 (~133 diffs) and E042 (~29 diffs) grid artifacts still drift vs goldens; not re-pinned.
- Deliberate re-pin of denominator masking at `src/portfolio_opt.py:445` (`y0 = w_feas / max(float(mu_s @ w_feas), 1e-12)`) is a separate, planned decision requiring ledger justification.

## Concrete Next Steps

1. Establish clean baseline: `SEED=42 bash scripts/check.sh` — all checks green.
2. Confirm tree state: `git status --short` — only `__pycache__/*.pyc` allowed.
3. Recover if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
4. Investigate well-conditioned solver for small N (<=5 assets): exact KKT enumeration as reference; CVXOPT/OSQP/custom active-set as stable alternative; preserve feasibility-validation invariant.
5. Validate: run E041/E042 lead drivers offline with `SEED=42 QUANT_RESEARCH_OFFLINE=1`; compare vs goldens at same tolerances.
6. Document findings in `ledger/RESEARCH_LEDGER.md`; re-pin goldens only via `scripts/check_golden_baseline.py --update` with rationale.

## Constraints (Do Not Violate)

- Always use `SEED=42`.
- Never leave `run_all_verification.py` half-finished.
- Do **not** re-pin goldens/`ledger/golden_baseline.json`/`ledger/data_baseline.json` to silence drift without ledger justification.
- Do **not** commit verification outputs; only intentional source/data changes.
- Follow `AGENTS.md`; honor "judge answer on problem constraints, not solver status" invariant.
- No goalpost moves; decisions unchanged unless evidence forces (pre-registered).

## Quick Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py        # quick (~8 min)
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e041.py
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e042_lead.py
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Files

- `src/portfolio_opt.py` — tangency QP, feasibility checks
- `tests/test_portfolio_opt.py` — invariant tests
- `ledger/RESEARCH_LEDGER.md` — E049 details
- `scripts/check.sh`, `run_all_verification.py`
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`
