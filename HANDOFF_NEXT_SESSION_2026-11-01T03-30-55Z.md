# Handoff - Initial Task - 2026-11-01T03:30:55Z

Durable detail: `.handoff/20261101T033055Z_INITIAL_TASK.md`

## Baseline status (verified this session at 2026-11-01T03:30:55Z)

`SEED=42 bash scripts/check.sh` → **EXIT 0, "=== All checks passed ==="**.
Working tree clean except untracked/modified `__pycache__/*.pyc` (bytecode only,
no source changes). No `.verify_snapshot/` pending. HEAD = `55dc549` chore(kilo):
checkpoint agent session.

The "FAIL" lines in check.sh output are **negative test fixtures** (intentional
malformed inputs in `tests/test_goldens_guard.py`, `tests/test_data_coverage.py`,
`tests/test_json_guard.py`) — they assert that the guards *do* fail on bad input.
They are not baseline failures; the suite's own summary line is green.

## Initial task for next agentic session

**START HERE:** Baseline is confirmed clean. No recovery needed. Before making
any source change, re-run `SEED=42 bash scripts/check.sh` to confirm it stays
green, then run `python3 -m py_compile` on every touched file.

## Quick context

- Repo: Quantitative-Trading-Public-Research-Prompted. Research phase complete
  (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Goldens in `experiments/*.json` are canonical; verification backs up/restores
  via `.verify_snapshot/`. Never overwrite via verification; never re-pin to
  silence numeric drift.
- If interrupted, restore before committing:
  `SEED=42 python3 run_all_verification.py --restore-only`
  (or `git checkout -- experiments/`).
- Seed is always `SEED=42`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.

## Open item to carry forward (ledger E049)

The tangency QP in `src/portfolio_opt.py` is still ill-conditioned: E041/E042
grid artifacts drift by 29–133 numeric differences vs their goldens (1-ulp
sensitivity). The solver's *exit status* defect is fixed and pinned by
`tests/test_portfolio_opt.py`; the residual conditioning is **documented, not
fixed**. Do **not** re-pin those goldens. The documented next step is a
research-engineering decision: replace the SLSQP tangency solves with a
well-conditioned deterministic solver (for N <= 5, exact active-set enumeration
of all KKT points — already used as the reference oracle — is feasible), then
deliberately re-pin the affected artifacts. A second known defect
(`src/portfolio_opt.py:253`, `y0 = w_feas / max(mu_s'w_feas, 1e-12)` masking a
negative denominator) is deliberately **not** fixed because fixing it would
change published numbers.

## Constraints

- Do not commit verification output; restore goldens if the working tree is
  dirty from an interrupted run.
- Do not re-pin goldens as a side effect of verification — only via
  `python3 scripts/check_golden_baseline.py --update` with justification.
- Data coverage is an enforced invariant (`ledger/data_baseline.json`). Any new
  `data.download()` call requires committing the file and re-pinning.
- The CI gate (`.github/workflows/verification-gate.yml`) cannot be created by
  automated agents; a copyable template is at
  `.github/workflow-templates/verification-gate.yml`.