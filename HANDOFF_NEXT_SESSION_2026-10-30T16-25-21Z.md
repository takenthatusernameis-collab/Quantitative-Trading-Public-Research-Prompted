# Durable Handoff — Next Agentic Session

**Timestamp:** 2026-10-30T16:25:21Z
**Branch:** `main` (up to date with `origin/main`)
**Working tree:** clean except `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/` `.pyc` files (compiled artifacts, not source). No uncommitted source changes.
**Last commits:** `d5bfb62`, `11b4909`, `465cdf6`, `35112b5` (all `chore(kilo): checkpoint agent session`).

## Initial task message (this handoff)

> **Task: Replace the SLSQP tangency-QP solves in `src/portfolio_opt.py` with a well-conditioned deterministic solver (exact active-set enumeration of all KKT points for N ≤ 5), then deliberately re-pin the affected artifacts. Do NOT re-pin to silence drift without the solver change. No research conclusion may change.**

See `HANDOFF_NEXT_SESSION_2026-10-30T16-14-49Z.md` for full context, open items, verification commands, and rules (E041 residual drift 133 numeric; E042-primary 56; E042 grid 42; E041 grid 29; second defect at `src/portfolio_opt.py:253` deliberately left unfixed).

## Verification commands (run BEFORE declaring done)

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Primary gate (~8 min; must be green)
SEED=42 python3 run_all_verification.py

# Confirm no stray source changes; pycache .pyc noise is expected/ignorable
git status --short | grep -v __pycache__
```

## Rules (from AGENTS.md)

- Always use `SEED=42`. Never move goalposts, change tolerances/drivers/skips, or change research decisions as a side effect of verification.
- `experiments/*.json` are canonical; `run_all_verification.py` backs up and restores them — never commit verification output. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Replacing an artifact requires deliberate `scripts/check_golden_baseline.py --update` so the replacement is in the diff.
- Offline mode: `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard (cache coverage invariant enforced by `scripts/check_data_coverage.py`).
- Python 3; no separate linter — run `python3 -m py_compile` on changed files.
- CI workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml`.

## Handoff outcome

Once the deterministic KKT-enumeration solver lands, the primary gate is green, and every re-pin is visible in the diff with no research conclusion changed, the session is done.
