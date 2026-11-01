# Initial Task - $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Baseline Status (verified at $(date -u +%Y-%m-%dT%H:%M:%SZ))
`SEED=42 bash scripts/check.sh` → **EXIT 0, "=== All checks passed ==="**
Working tree clean (only untracked `__pycache__/*.pyc`). No `.verify_snapshot/` pending.
HEAD = `55dc549` chore(kilo): checkpoint agent session.

The "FAIL" lines are intentional negative test fixtures in `tests/test_goldens_guard.py`, `tests/test_data_coverage.py`, `tests/test_json_guard.py` — they verify guards properly reject bad inputs. Not baseline failures.

## Initial Task for Next Agentic Session
**START HERE:** Baseline confirmed clean. Before making any source changes:
1. Re-run `SEED=42 bash scripts/check.sh` to confirm it stays green.
2. Run `python3 -m py_compile` on every touched file.
3. Follow project constraints (never commit verification output, never re-pin goldens as side effect of verification).

## Quick Context
- Repo: Quantitative-Trading-Public-Research-Prompted. Research phase complete (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Goldens in `experiments/*.json` are canonical; verification backs up/restores via `.verify_snapshot/`. Never overwrite via verification; never re-pin to silence numeric drift.
- If interrupted, restore before committing: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- Seed always `SEED=42`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Data coverage enforced via `ledger/data_baseline.json`; any new `data.download()` requires committing file + re-pinning.
- CI gate cannot be created by automated agents (template at `.github/workflow-templates/verification-gate.yml`).

## Open Item to Carry Forward (ledger E049)
Tangency QP in `src/portfolio_opt.py` remains ill-conditioned: E041/E042 grid artifacts drift 29–133 numeric differences vs goldens (1-ulp sensitivity). Solver exit-status defect fixed and pinned by `tests/test_portfolio_opt.py`. Residual conditioning is **documented, not fixed** — do **not** re-pin goldens. Documented next step: replace SLSQP tangency solves with well-conditioned deterministic solver (for N<=5, exact active-set enumeration already used as reference oracle is feasible), then deliberately re-pin affected artifacts. Deliberately NOT fixing `src/portfolio_opt.py:253` (`y0 = w_feas / max(mu_s'w_feas, 1e-12)`) to avoid changing published numbers.

## Constraints
- Do not commit verification output; restore goldens if working tree dirty from interrupted run.
- Do not re-pin goldens as side effect of verification — only via `python3 scripts/check_golden_baseline.py --update` with justification.
- Data coverage is enforced invariant. Any new `data.download()` call requires committing the file and re-pinning.
- CI gate template exists but cannot be auto-created.
