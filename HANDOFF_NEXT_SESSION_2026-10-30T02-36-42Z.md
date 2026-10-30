# Durable Handoff for Next Agentic Work Session

**Handoff written:** 2026-10-30T02:36:42Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**Session type:** handoff-only (no source changes made, no verification run executed)

---

## INITIAL TASK (start here)

**Verify repository stability before any new work, then continue the open E049 follow-up item: address tangency QP ill-conditioning so the E041/E042 grid artifacts reproduce within tolerance, without reintroducing solver-status dependence.**

Concretely, the next session should:
1. Establish a clean baseline: `SEED=42 bash scripts/check.sh` — all checks must be green before touching any source.
2. Confirm tree state: `git status --short` — only `__pycache__/*.pyc` modifications are allowed.
3. If a prior verification run was interrupted, recover first: `SEED=42 python3 run_all_verification.py --restore-only`.
4. Investigate a well-conditioned solver for the small-N (<=5 assets) tangency QP:
   - Exact KKT / active-set enumeration as a reference answer.
   - CVXOPT or OSQP, or a custom active-set solver, as a stable alternative.
   - Preserve the E049 invariant: judge the answer on the problem's constraints, never on the solver's `success`/exit status.
5. Validate the change: run the E041 and E042 lead drivers offline
   (`SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e041.py` and `run_e042_lead.py`)
   and compare against the committed goldens at the same tolerances.
6. Document findings in `ledger/RESEARCH_LEDGER.md`. Re-pin goldens only via
   `python3 scripts/check_golden_baseline.py --update`, with a ledger-justified rationale.

---

## CONTEXT

- Research phase is complete (E001–E043). Surviving validated strategies are documented
  in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are the canonical golden artifacts. The verification suite
  backs them up before re-running and restores them afterwards; the baseline is
  never modified by verification. A live run owns `.verify_snapshot/ACTIVE.json`.
- Optimizer determinism fix (E049) is in place: `src/portfolio_opt.py` validates a
  solver answer against the problem's constraints, never against the solver's exit
  status. `tests/test_portfolio_opt.py` encodes this invariant and is a first-class
  step of `scripts/check.sh`.
- Remaining open item: the tangency QP itself is ill-conditioned — a 1-ulp input
  perturbation moves the `min_var` answers by ~1e-05. E041 (~133 numeric diffs) and
  E042 (~29 numeric diffs) grid artifacts still drift vs their goldens. Per ledger
  guidance, do **not** re-pin them to silence that drift.
- A separate, planned decision — deliberate denominator masking at
  `src/portfolio_opt.py:445` (`y0 = w_feas / max(float(mu_s @ w_feas), 1e-12)`) —
  also requires ledger justification before implementation.
- E029 and E030 are now offline-reproducible (pinned fundamentals snapshot / ETF panel).
- Cache coverage is an enforced invariant (`scripts/check_data_coverage.py`); the
  verification suite re-executes every driver with `QUANT_RESEARCH_OFFLINE=1`.

---

## CONSTRAINTS (do not violate)

- Always use `SEED=42`.
- Never leave `run_all_verification.py` half-finished; recover with `--restore-only`.
- Do **not** re-pin goldens, `ledger/golden_baseline.json`, or
  `ledger/data_baseline.json` to silence drift without explicit ledger justification.
- Do **not** commit verification outputs; only intentional source/data changes.
- Honor the E049 invariant: judge the optimizer answer on problem constraints, not
  solver status.
- No goalpost moves; decisions unchanged unless evidence forces (pre-registered).

---

## QUICK COMMANDS

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended    # extended (~21 min)
SEED=42 python3 run_all_verification.py --full        # full (~15 min)
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e041.py
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e042_lead.py
SEED=42 python3 run_all_verification.py --restore-only
```

---

## KEY FILES

- `src/portfolio_opt.py` — tangency QP, feasibility validation, denominator masking at line 445
- `tests/test_portfolio_opt.py` — optimizer invariant tests (first-class check.sh step)
- `ledger/RESEARCH_LEDGER.md` — E049 details and open items
- `scripts/check.sh`, `run_all_verification.py`
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`

---

(End of file)