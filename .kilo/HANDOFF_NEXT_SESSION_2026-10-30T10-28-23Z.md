# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-30T10:28:23Z (UTC)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `ddebff3` (HEAD; checkpoint commit)
**Working tree:** clean (no source/data changes pending, no untracked modifications).
**Snapshot state:** `.verify_snapshot/` does **NOT** exist — no stale or active snapshot. No recovery needed before a verification run.

This session left a durable initial task message for the next agentic work session. No source changes were made and no verification run was executed.

## Initial Task (Start Here)

**Task:** Baseline integrity first, then address the standing E049 follow-up (tangency QP ill-conditioning) so E041/E042 grid artifacts reproduce within tolerance without reintroducing solver-status dependence.

## Concrete Next Steps

1. **Confirm clean baseline:** `SEED=42 bash scripts/check.sh` — expect exit 0 (py_compile, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `tests/test_portfolio_opt.py`). No snapshot recovery is required this time.

2. **Confirm tree state:** `git status --short` — clean / only `__pycache__/*.pyc` allowed.

3. **Quick verification:** `SEED=42 python3 run_all_verification.py --skip-slow` (~8 min offline) to re-execute the 5a-block drivers and compare vs goldens.

4. **Investigate well-conditioned solver for small N (<=5 assets):** exact KKT enumeration as reference; CVXOPT/OSQP/custom active-set as stable alternative; preserve the feasibility-validation invariant (judge answer on problem constraints, not solver status).

5. **Validate:** run E041/E042 lead drivers offline with `SEED=42 QUANT_RESEARCH_OFFLINE=1`; compare vs goldens at same tolerances.

6. **Document findings:** update `ledger/RESEARCH_LEDGER.md`; re-pin goldens only via `scripts/check_golden_baseline.py --update` with rationale.

## Context

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Optimizer determinism fix (E049) is in place: `src/portfolio_opt.py` validates answers against problem constraints, not solver `success` status; `tests/test_portfolio_opt.py` passes and is integrated into `scripts/check.sh`.
- Remaining open item: tangency QP is ill-conditioned (1-ulp perturbations move `min_var` answers by ~1e-5). E041 (~133 diffs) and E042 (~29 diffs) grid artifacts still drift vs goldens; not re-pinned.
- E029 and E030 are offline-reproducible with 0 differences (pinned inputs).

## Constraints (Do Not Violate)

- Always use `SEED=42`. Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`); all required caches must be present and pinned.
- Never leave `run_all_verification.py` half-finished.
- Do **not** re-pin goldens/`ledger/golden_baseline.json`/`ledger/data_baseline.json` to silence drift without ledger justification.
- Do **not** commit verification outputs; only intentional source/data changes.
- Follow `AGENTS.md`; honor "judge answer on problem constraints, not solver status" invariant.
- No goalpost moves; decisions unchanged unless evidence forces (pre-registered).
- Do **not** commit changes without explicit user direction.

## Quick Commands

```bash
SEED=42 bash scripts/check.sh                              # baseline integrity
SEED=42 python3 run_all_verification.py --skip-slow        # quick verification (~8 min)
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e041.py
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e042_lead.py
```

## Key Files

- `src/portfolio_opt.py` — tangency QP, feasibility checks
- `tests/test_portfolio_opt.py` — invariant tests
- `ledger/RESEARCH_LEDGER.md` — E049 details, open items
- `scripts/check.sh`, `run_all_verification.py`
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned baselines (present, unmodified)

## Handoff Notes

- This file is the durable handoff target. Symlinks in `.kilo/` (`HANDOFF.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md`, `handoff.md`, `handoff_next.md`, `handoff_next_session.md`) must point to this file: `HANDOFF_NEXT_SESSION_2026-10-30T10-28-23Z.md`.
- Archived copy: `.kilo/handoffs/HANDOFF-2026-10-30T10-28-23Z.md`.
- Preceding handoff: `.kilo/handoffs/HANDOFF-2026-10-30T09-26-56Z.md`.
