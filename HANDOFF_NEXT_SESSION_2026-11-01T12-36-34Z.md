# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T12-36-34Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `1cdef3f` (chore(kilo): checkpoint agent session)
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session

1. `pip install -r requirements.txt` if the environment was reset.
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with `=== All checks passed ===`.
3. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain. Do NOT commit verification output.
4. Only after steps 1–3 pass cleanly, address the standing open item below. Do not re-pin goldens to silence drift.

## Baseline-integrity note (carried forward)

The interrupted-run recovery (`SEED=42 python3 run_all_verification.py --restore-only`) cleared the stale `.verify_snapshot/` marker. The working tree matches the pinned baseline for all 107 artifacts; the 3 HEAD-only mismatches (`experiments/cointegration_large_liquid.json`, `experiments/dollar_neutral_lowbeta_large_liquid.json`, `experiments/pairs_large_liquid.json`, ~1e-16 `corr_spy` drift) are expected. The pinned baseline is the authoritative record. **Do not `git checkout -- experiments/`**.

## Standing open item (highest value)

**E049 tangency QP ill-conditioning** (`src/portfolio_opt.py`, `max_sharpe` branch). SLSQP at `ftol=1e-12` is chaotically ill-conditioned: a 1-ulp covariance perturbation moves OOS Sharpe by up to 3e-02. E041/E042 artifacts still drift vs goldens by 29–133 numeric diffs.

Do NOT re-pin to silence. Intended fix:

- Route `max_sharpe` through `exact_qp` / `exact_tangency_kkt` active-set enumeration (N ≤ 5 feasible; reference oracle used in E049).
- Fix the `y0 = w_feas / max(mu_s'w_feas, 1e-12)` start point at `src/portfolio_opt.py:253`.
- After the fix, re-run `experiments/run_e041.py`, `experiments/run_e042.py`, `experiments/run_e042_lead.py`, and re-pin deliberately with `python3 scripts/check_golden_baseline.py --update`, recording the change in the ledger.

## Constraints

- Never commit verification output. Restore goldens first if interrupted.
- Never re-pin goldens to silence drift.
- Run `python3 -m py_compile` on changed files.
