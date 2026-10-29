# Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-10-29T19-59-30Z
**Status:** Baseline integrity restored after interrupted-run recovery; durable initial task message for next session.

## Initial Task Message (START HERE)

> Repository baseline is verified and stable. **No new research is warranted.**
> Your primary task is to verify stability by running the extended verification suite, confirm the pre-existing known drifts remain unchanged, and report results.
> **Do not modify goldens, weaken tolerances, or change any gate logic.**
> If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
> All constraints from below still apply.

## What Was Just Done (this session)

- Discovered a **stale `.verify_snapshot/`** owned by a dead pid 39093 (elapsed 00:00, not running). Its 107 experiment copies matched the pinned `ledger/golden_baseline.json` fingerprints exactly — i.e. the snapshot held the *canonical* goldens, not a half-finished run.
- Working tree had **2 files modified vs the golden pin** (an interrupted run had written into `experiments/`):
  - `experiments/blend_tsm_dnlowbeta_large_liquid.json` (golden `61c0e53a…` → working tree `03f9937e…`)
  - `experiments/pairs_large_liquid.json` (golden `5ab39998…` → working tree `534c4b13…`)
- **Restored both from `.verify_snapshot/experiments/`**. Re-checked all 107 pinned files: **0 golden drifts**.
- `git diff --stat HEAD -- experiments/` is empty; no untracked files in `experiments/`. The baseline is clean and identical to HEAD.
- Did **not** run the verification suite itself (left to the next session, per the standing task).

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

## Known Pre-Existing Drift (reporting-only, decisions unchanged)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.
- **E041/E042 sensitivity grids and full E042 confirmatory golden**: not byte-reproducible in this sandbox due to residual 1-ulp sensitivity of the ill-conditioned tangency QP. No structural differences; no gate or decision affected. Do NOT re-pin — see ledger E049 and `HANDOFF_REPRO_CAVEAT.md`.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/` per `data/fundamentals_vintages.json`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).
- Do not commit `__pycache__/*.pyc` — tracked but drift by mtime only; leave unstaged.
- Do not re-pin goldens or data baselines unless there is an explicit, documented need (current disposition: committed golden is authoritative).

## Candidate Next Research Tasks (unstarted; only if explicitly requested)

Per prior handoffs, highest-value unstarted: **Optimize TSM+DN blend weights and evaluate adding a diversifier (E050+)**. If this is requested later, pre-register with gates and falsification expectations in `ledger/RESEARCH_LEDGER.md` before running. Prerequisites exist (`src/strategies.py`, `src/backtest.py`, cached data). This is not part of the stability verification task above.

## Prerequisites

- Dependencies installed (`pip install -r requirements.txt`: numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional (fallback to `scipy.optimize`).
- Working tree clean (aside `__pycache__/*.pyc` mtime drift).
- `SEED=42` for all verification commands.
- `.verify_snapshot/` present and consistent with `ledger/golden_baseline.json` (107 files, 0 drifts).