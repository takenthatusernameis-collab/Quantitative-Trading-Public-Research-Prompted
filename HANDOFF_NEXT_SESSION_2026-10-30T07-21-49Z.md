# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-30T07:23:08Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `7c1cc90`
**Working tree:** clean except `__pycache__/*.pyc` modifications (tracked bytecode caches; no source changes).
**Snapshot:** `.verify_snapshot/ACTIVE.json` exists with dead PID 33924 (stale). Recovery required before any verification run.

## INITIAL TASK (START HERE)

**Task:** Recover the stale verification snapshot, establish a clean baseline, then continue the open E049 follow-up — address tangency QP ill-conditioning so `E041`/`E042` grid artifacts reproduce within tolerance without reintroducing solver-status dependence.

## Concrete Next Steps (In Order)

1. **Recover stale snapshot (BLOCKING):**
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   (or `git checkout -- experiments/` as last resort). Never leave a verification run half-finished.

2. **Establish clean baseline:**
   ```bash
   git status --short
   SEED=42 bash scripts/check.sh
   ```
   All checks must pass. Only `__pycache__/*.pyc` should remain if anything.

3. **Reproduce the current drift:**
   ```bash
   SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e041.py
   SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e042_lead.py
   ```
   Compare against committed goldens at existing tolerances (expect ~133 diffs on E041, ~29 on E042).

4. **Investigate well-conditioned solver for small N (≤5 assets):**
   - Consider exact KKT enumeration as reference
   - Evaluate stable alternatives (CVXOPT/OSQP/custom active-set)
   - **Preserve the feasibility-validation invariant:** validate answers against problem constraints, never gate on solver `success`/status
   - Do not reintroduce environment-dependent solver-status checks (see E049 fix in `src/portfolio_opt.py`)

5. **Validate and document:**
   - Re-run E041/E042 offline with `SEED=42 QUANT_RESEARCH_OFFLINE=1` and confirm drift is within tolerance
   - Update `ledger/RESEARCH_LEDGER.md` with findings
   - Re-pin goldens **only** via `python3 scripts/check_golden_baseline.py --update` with explicit rationale. Do **not** re-pin to silence numerical drift without justification.

## Context

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Optimizer determinism fix (E049) in place: `src/portfolio_opt.py` validates answers against problem constraints, not solver `success` status; `tests/test_portfolio_opt.py` passes.
- Remaining open item: tangency QP ill-conditioned (1-ulp perturbations move `min_var` answers by ~1e-5). E041 (~133 diffs) and E042 (~29 diffs) grid artifacts still drift vs goldens; not re-pinned.
- E029 and E030 are offline-reproducible with 0 differences (pinned inputs/caches).

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

- This is the durable handoff for the next agentic session.
- Previous handoff: `handoff_next_session.md` (2026-10-30T07:21:49Z).
