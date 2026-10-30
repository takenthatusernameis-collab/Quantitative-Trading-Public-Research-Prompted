# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-30T07:21:49Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `7c1cc90`
**Working tree:** clean except `__pycache__/*.pyc` modifications (tracked bytecode caches; no source changes).
**Snapshot:** `.verify_snapshot/ACTIVE.json` exists with dead PID 33924 (stale). Recovery required before any verification run.

This session inspected repository state and created this durable handoff. No source changes were made and no verification run was executed.

## Initial Task (Start Here)

**Task:** Recover the stale verification snapshot, establish a clean baseline, then continue the open E049 follow-up item — address tangency QP ill-conditioning so E041/E042 grid artifacts reproduce within tolerance without reintroducing solver-status dependence.

## Concrete Next Steps

1. **Recover stale snapshot (BLOCKING, do first):** `.verify_snapshot/` is stale (dead PID 33924). Recover before starting any verification run:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   (or `git checkout -- experiments/` as last resort). Never leave a verification run half-finished.
2. **Establish clean baseline:** `SEED=42 bash scripts/check.sh` — all checks green.
3. **Confirm tree state:** `git status --short` — only `__pycache__/*.pyc` allowed after recovery.
4. **Investigate well-conditioned solver for small N (<=5 assets):** exact KKT enumeration as reference; CVXOPT/OSQP/custom active-set as stable alternative; preserve feasibility-validation invariant.
5. **Validate:** run E041/E042 lead drivers offline with `SEED=42 QUANT_RESEARCH_OFFLINE=1`; compare vs goldens at same tolerances.
6. **Document findings:** update `ledger/RESEARCH_LEDGER.md`; re-pin goldens only via `scripts/check_golden_baseline.py --update` with rationale.

## Context

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Optimizer determinism fix (E049) in place: `src/portfolio_opt.py` validates answers against problem constraints, not solver `success` status; `tests/test_portfolio_opt.py` passes.
- Remaining open item: tangency QP ill-conditioned (1-ulp perturbations move `min_var` answers by ~1e-5). E041 (~133 diffs) and E042 (~29 diffs) grid artifacts still drift vs goldens; not re-pinned.
- E029 and E030 offline-reproducible with 0 differences (pinned inputs).

## Constraints (Do Not Violate)

- Always use `SEED=42`. Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`).
- Never leave `run_all_verification.py` half-finished.
- Do not re-pin goldens/baselines to silence drift without ledger justification.
- Do not commit verification outputs; only intentional source/data changes.
- Do not commit changes without explicit user direction.

## Quick Commands

```bash
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e041.py
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e042_lead.py
```

## Key Files

- `src/portfolio_opt.py` — tangency QP, feasibility checks
- `tests/test_portfolio_opt.py` — invariant tests
- `ledger/RESEARCH_LEDGER.md` — E049 details, open items
- `scripts/check.sh`, `run_all_verification.py`
- `.verify_snapshot/ACTIVE.json` — stale (dead PID 33924), recover before running

## Handoff Notes

- This file is the durable handoff target. Preceding handoff: `HANDOFF_NEXT_SESSION_2026-10-30T06-33-24Z.md`.
