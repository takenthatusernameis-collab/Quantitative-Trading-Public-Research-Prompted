# Durable Handoff — Next Agentic Session

**Timestamp:** 2026-10-30T15:16:33Z
**Branch:** `main` (up to date with origin/main)
**Working tree:** clean except pycache files (gitignored, not source)
**Last commits:** checkpoint commits on `main` (most recent faf0a27)

## Repository state

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Market-neutral-total-portfolio line is CLOSED.
- `src/portfolio_opt.py`: exact active-set KKT solver (`exact_qp`, `exact_tangency_kkt`) is the primary path for `max_sharpe` and `min_var`; SLSQP fallback only when exact enumeration finds no KKT point. Feasibility judged on problem constraints (E049 fix preserved), never solver exit status.
- Canonical artifacts: `experiments/*.json` are golden baselines (SHA-256 pinned in `ledger/golden_baseline.json`); verification suite backs them up and restores them.
- Data caches pinned per `ledger/data_baseline.json` / `data/fundamentals_vintages.json`; enforced by `scripts/check_data_coverage.py` under `QUANT_RESEARCH_OFFLINE=1`.
- No live verification snapshot (`.verify_snapshot/` absent, no `ACTIVE.json`). No run in progress; nothing to recover.

## Initial Task (Start Here)

Re-verify repository stability; no new research is warranted.

1. Run `SEED=42 bash scripts/check.sh` (fast convention check + tests + goldens). Expect exit 0 with only the pre-existing E030/E041 drift unchanged. Do NOT weaken tolerances, skip drivers, or modify committed goldens.
2. Optionally confirm the deterministic-solver item from `HANDOFF-2026-10-30T15-15-10Z.md`: verify the exact KKT path (not SLSQP) is the effective solver for the tangency QP (N ≤ 5) on every rebalance fold; keep `_tangency_feasible` constraint-based validation. No research conclusions may change. If any golden changed, re-pin deliberately via `scripts/check_golden_baseline.py --update` so the replacement appears in the diff; do NOT re-pin to silence drift without a solver change. Affected candidates: E041 portfolio/grid, E042 primary/grid.
3. Confirm `git status --short | grep -v __pycache__` shows only intended changes. If a verification run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Known pre-existing drift (reporting-only, decisions unchanged — do NOT re-pin)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone.
- **E030**: numeric diffs on near-zero quantities (documented).
- E029/E030 inputs are pinned for offline reproducibility; goldens deliberately re-pinned.

## Hard Rules

- Always `SEED=42`. Never move goalposts, change tolerances/drivers/skips, or change research decisions as a side effect of verification.
- `experiments/*.json` are canonical; never commit verification output.
- Replacing an artifact requires deliberate `scripts/check_golden_baseline.py --update` (visible in diff).
- Run `python3 -m py_compile` on changed files; no separate linter configured.
- Offline mode: `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard.
- CI workflow cannot be created by agents (controller restores `.github/workflows/`; template at `.github/workflow-templates/verification-gate.yml`).

**Start here:** Read `src/portfolio_opt.py` around `exact_qp`/`optimize_portfolio_weights` (lines 226–492) and `tests/test_portfolio_opt.py`, then run `SEED=42 bash scripts/check.sh`.
