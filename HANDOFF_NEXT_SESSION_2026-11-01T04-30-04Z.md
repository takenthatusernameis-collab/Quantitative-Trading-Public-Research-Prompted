# Handoff — 2026-11-01T04:30:04Z

## INITIAL TASK FOR THE NEXT AGENTIC SESSION (start here)

**Goal: Establish a clean, verified baseline before making any changes.**

Execute in order:

1. [ ] **Check repo state** — `git status && git log -1 --oneline`
2. [ ] **Run fast integrity check** — `SEED=42 bash scripts/check.sh`
   - Confirm `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` pass
   - Confirm `scripts/check_data_coverage.py` passes
   - Confirm tests pass (`python3 -m py_compile` on changed files + `tests/test_portfolio_opt.py`)
   - NOTE: the "FAIL" lines in `check.sh` output are intentional negative test fixtures in
     `tests/test_goldens_guard.py`, `tests/test_data_coverage.py`, `tests/test_json_guard.py`
     (they verify guards properly reject bad inputs). The script exits 0.
3. [ ] **Recover if needed** — if goldens differ from HEAD or a snapshot is stale, run
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
   Never proceed with modified goldens.
4. [ ] **Review open items** — read `ledger/RESEARCH_LEDGER.md`, especially E049
   (optimizer determinism). E041/E042 grid artifacts may still drift numerically due to
   an ill-conditioned QP — do **not** re-pin them to silence that.
5. [ ] **Report baseline status** — summarize pass/fail and confirm baseline clean before new work.

## Baseline Status (verified at 2026-11-01T04:30:04Z)

`SEED=42 bash scripts/check.sh` → **EXIT 0, "=== All checks passed ==="**
Working tree clean (only untracked `__pycache__/*.pyc`). No `.verify_snapshot/` pending.
HEAD = `ee72ede` chore(kilo): checkpoint agent session.

## Project State

- Repo: Quantitative-Trading-Public-Research-Prompted. Research phase complete (E001–E049).
  Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Goldens in `experiments/*.json` are canonical; verification backs up/restores via
  `.verify_snapshot/`. Never overwrite via verification; never re-pin to silence numeric drift.
- If interrupted, restore before committing: `SEED=42 python3 run_all_verification.py --restore-only`
  or `git checkout -- experiments/`.
- Seed always `SEED=42`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Data coverage enforced via `ledger/data_baseline.json`; any new `data.download()` requires
  committing the file and re-pinning.
- CI gate cannot be created by automated agents (template at
  `.github/workflow-templates/verification-gate.yml`).

## Open Item to Carry Forward (ledger E049)

Tangency QP in `src/portfolio_opt.py` remains ill-conditioned: E041/E042 grid artifacts drift
29–133 numeric differences vs goldens (1-ulp sensitivity). The solver exit-status defect is
fixed and pinned by `tests/test_portfolio_opt.py`. Residual conditioning is **documented, not
fixed** — do **not** re-pin goldens. Documented next step: replace SLSQP tangency solves with a
well-conditioned deterministic solver (for N<=5, exact active-set enumeration already used as a
reference oracle is feasible), then deliberately re-pin affected artifacts. Deliberately NOT
fixing `src/portfolio_opt.py:253` (`y0 = w_feas / max(mu_s'w_feas, 1e-12)`) to avoid changing
published numbers.

## Constraints

- Always use `SEED=42`.
- Do not commit verification output; restore goldens if working tree dirty from an interrupted run.
- Do not re-pin goldens as a side effect of verification — only via
  `python3 scripts/check_golden_baseline.py --update` with justification.
- Data coverage is enforced invariant. Any new `data.download()` call requires committing the file and re-pinning.
- CI gate template exists but cannot be auto-created.
