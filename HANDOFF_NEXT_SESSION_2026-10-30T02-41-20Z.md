# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-30T02:41:20Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**Last commit:** 50da76822b2db6ca0882215d63c4f1567b05b62d (2026-10-30 02:41:12 +0000, "chore(kilo): checkpoint agent session")
**Working tree:** clean (only `__pycache__/*.pyc` modified; no source/data changes this session).

This session only inspected the repository and produced this durable handoff. No source
changes were made and no verification run was executed, so the canonical goldens under
`experiments/` are untouched and `ledger/golden_baseline.json` still pins them.

## Initial Task (Start Here)

**Task:** Continue the open E049 follow-up item — address tangency QP ill-conditioning so
E041/E042 grid artifacts reproduce within tolerance without reintroducing solver-status
dependence. Verify repository stability first.

## Context

- Research phase complete (E001–E049). Surviving validated strategies documented in
  `ledger/RESEARCH_LEDGER.md` (see the E049 entry at the end of the file, lines ~4805–4989).
- Optimizer determinism fix (E049) is in place: `src/portfolio_opt.py` validates answers
  against the problem's constraints, never the solver's `success` exit status;
  `tests/test_portfolio_opt.py` (5 tests) passes and is a first-class step of
  `scripts/check.sh`.
- Remaining open item: the tangency QP itself is still ill-conditioned. A 1-ulp input
  perturbation moves `min_var` answers by up to ~2.6e-05, so E041 (~133 numeric diffs)
  and E042 (~29–42 diffs) grid artifacts still drift vs their goldens. These were
  deliberately **not** re-pinned (re-pinning would bake this machine's numbers over an
  unfixed defect).
- A second, smaller defect was found and deliberately **not** fixed in E049:
  `src/portfolio_opt.py:445` (`y0 = w_feas / max(float(mu_s @ w_feas), 1e-12)`) masks a
  *negative* denominator. Fixing the start point (a max-`mu_s'w` LP on the feasible
  simplex) would make SLSQP converge to the exact optimum at the 2019-10-16 rebalance
  and **change the published numbers**, so it is left for the same deliberate re-pin
  decision.
- The reference oracle already used during E049 was an exact active-set enumeration of all
  KKT points for N <= 5 — that is the candidate well-conditioned solver to port.

## Concrete Next Steps

1. Establish clean baseline: `SEED=42 bash scripts/check.sh` — all checks green.
2. Confirm tree state: `git status --short` — only `__pycache__/*.pyc` allowed.
3. Recover if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
4. Port a well-conditioned, deterministic solver for the tangency QP
   (`min y'Sy s.t. mu'y = 1, y >= 0, |B'y| <= c 1'y`) for small N (<= 5 assets):
   exact KKT active-set enumeration as the primary path, CVXOPT/OSQP or a custom
   active-set as a stable fallback. Preserve the E049 invariant: judge the answer on
   the problem's constraints, never on the solver's exit status.
5. Validate: run E041/E042 lead drivers offline with `SEED=42 QUANT_RESEARCH_OFFLINE=1`;
   compare vs goldens at the same tolerances (`numeric_tol=1e-4`).
6. Document findings in `ledger/RESEARCH_LEDGER.md`; re-pin goldens only via
   `python3 scripts/check_golden_baseline.py --update` with explicit rationale.

## Constraints (Do Not Violate)

- Always use `SEED=42`.
- Never leave `run_all_verification.py` half-finished (it backs up and restores
  `experiments/*.json` automatically; the `.verify_snapshot/` marker holds the owning pid).
- Do **not** re-pin goldens / `ledger/golden_baseline.json` / `ledger/data_baseline.json`
  to silence drift without ledger justification.
- Do **not** commit verification outputs; only intentional source/data changes.
- Honor the E049 invariant: judge the answer on the problem constraints, not the
  solver's status (`tests/test_portfolio_opt.py` pins it).
- No goalpost moves; research decisions unchanged unless evidence forces (pre-registered).

## Quick Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended    # ~21 min
SEED=42 python3 run_all_verification.py --full        # ~15 min
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e041.py
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e042_lead.py
SEED=42 python3 run_all_verification.py --restore-only
python3 scripts/check_golden_baseline.py --update     # deliberate re-pin only
```

## Key Files

- `src/portfolio_opt.py` — tangency QP (`max_sharpe`), feasibility checks, the
  `_tangency_feasible` helper added in E049, and the `y0` start-point defect at line 445.
- `tests/test_portfolio_opt.py` — the solver-status invariant (first-class check).
- `ledger/RESEARCH_LEDGER.md` — E049 entry (end of file) and the full E001–E049 history.
- `scripts/check.sh`, `run_all_verification.py` — verification suite and gates.
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py` — golden guards.
- `experiments/e041_market_neutral_portfolio.json`, `experiments/e041_sensitivity_grid.json`,
  `experiments/e042_sensitivity_grid.json` — the drifting artifacts.

(End of file)