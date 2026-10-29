# Handoff for Next Agentic Work Session

**Created:** 2026-10-29T18:49:29Z
**Session Context:** Research phase complete (E001–E049). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Verification baseline integrity guards in place. Repository verified stable as of this handoff.

---

## Initial Task Message (START HERE)

> Repository is fully verified and in a stable state. **No new research is warranted.**
> Your primary task is to verify stability by running the extended verification suite, confirm the pre-existing known drifts remain unchanged, and report results.
> **Do not modify goldens, weaken tolerances, or change any gate logic.**
> If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
> All constraints from below still apply.

---

## Current State (verified at handoff time)

- **Branch:** `main`, up to date with `origin/main`. HEAD `0fd7049` (chore(kilo): checkpoint agent session).
- **Working tree:** clean of tracked changes. Only `__pycache__/*.pyc` may show mtime drift — tracked files; do not commit them.
- **No `.verify_snapshot/`** active; no untracked files; no stale verification output.
- **`experiments/*.json` goldens match HEAD.**
- **`SEED=42 bash scripts/check.sh` → ALL CHECKS PASSED** (goldens vs HEAD, stale-snapshot check, convention robustness, py_compile, data-coverage guard, golden-baseline fingerprint guard, template validation, experiment-script imports).
- **Research phase complete (E001–E049).** Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Latest committed work: **E049** (2026-10-20) — `src/portfolio_opt.py` solver-exit-status defect fixed, `tests/test_portfolio_opt.py` added, E042-lead artifact re-pinned. Research conclusions unchanged (E041 REJECTED, E042 PARTIAL).

---

## Precise Task (bounded)

Re-run the verification suite to confirm stability:

```bash
SEED=42 python3 run_all_verification.py --extended
```

Expect the pre-existing E030/E041 drift below. **Do not** weaken tolerances, skip drivers, or modify committed goldens. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

After completion, report:
1. Overall pass/fail of the extended suite
2. Confirmation that E030 and E041 drifts match the known pattern (counts and nature) with no new structural diffs
3. Any anomalies (snapshot active, golden drift vs HEAD, data coverage issues)
4. Final state recommendation (stable / needs attention)

---

## Known Pre-Existing Drift (reporting-only, decisions unchanged)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.
- **E041/E042 sensitivity grids and full E042 confirmatory golden**: not byte-reproducible in this sandbox due to residual 1-ulp sensitivity of the ill-conditioned tangency QP. No structural differences; no gate or decision affected. Do NOT re-pin — see ledger E049 and `HANDOFF_REPRO_CAVEAT.md`.

---

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/` per `data/fundamentals_vintages.json`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).
- Do not commit `__pycache__/*.pyc` — tracked but drift by mtime only; leave unstaged.
- Do not re-pin goldens or data baselines unless there is an explicit, documented need (current disposition: committed golden is authoritative).

---

## Candidate Next Research Tasks (unstarted; only if explicitly requested)

Per prior handoffs, highest-value unstarted: **Optimize TSM+DN blend weights and evaluate adding a diversifier (E050+)**. If this is requested later, pre-register with gates and falsification expectations in `ledger/RESEARCH_LEDGER.md` before running. Prerequisites exist (`src/strategies.py`, `src/backtest.py`, cached data). This is not part of the stability verification task above.

---

## Prerequisites

- Dependencies installed (`pip install -r requirements.txt`: numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional (fallback to `scipy.optimize`).
- Working tree clean (aside `__pycache__/*.pyc` mtime drift).
- `SEED=42` for all verification commands.
