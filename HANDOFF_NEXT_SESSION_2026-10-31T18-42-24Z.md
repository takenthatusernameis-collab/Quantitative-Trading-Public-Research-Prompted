# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-31T18:42:24Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main (HEAD = `e5452d4`)
**Working tree:** clean at handoff time except `__pycache__/*.pyc` (gitignored). No live verification run in progress (`.verify_snapshot/` absent).

## Initial Task (Start Here)

**Task:** Establish clean baseline (`SEED=42 bash scripts/check.sh`), then continue the open E049 follow-up — resolve tangency QP ill-conditioning so E041/E042 grid artifacts reproduce within tolerance, without reintroducing solver-status dependence.

## Constraints

- Use `SEED=42`. Never leave verification half-finished; recover via `SEED=42 python3 run_all_verification.py --restore-only`.
- Do not re-pin goldens without ledger justification. Do not commit verification outputs.
- Preserve the feasibility-validation invariant in `src/portfolio_opt.py` (validate on problem constraints, never on solver exit status — pinned by `tests/test_portfolio_opt.py`).
- Honor pinned cache vintages (`data/vintages.json`, `data/fundamentals/`).
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.

## Known Pre-Existing Drift (reporting-only, do not re-pin)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone.
- **E030**: numeric diffs on near-zero quantities (documented). Do not re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned.

## Quick Reference

```bash
SEED=42 bash scripts/check.sh            # fast convention + template validation
SEED=42 python3 run_all_verification.py --extended   # 18 committed drivers
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid
```