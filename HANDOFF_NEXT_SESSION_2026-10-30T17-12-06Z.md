# Durable Handoff — Next Agentic Session

**Timestamp:** 2026-10-30T17:12:06Z
**Branch:** `main` (up to date with `origin/main`)
**Working tree:** clean except `__pycache__/` `.pyc` files. No uncommitted source changes.

## Initial task message (this handoff)

> **Task: Replace the SLSQP tangency-QP solves in `src/portfolio_opt.py` with a well-conditioned deterministic solver (exact active-set enumeration of all KKT points for N ≤ 5), then deliberately re-pin the affected artifacts. Do NOT re-pin to silence drift without the solver change. No research conclusion may change.**

Open items: E041 residual drift 133 numeric; E042-primary 56; E042 grid 42; E041 grid 29; second defect at `src/portfolio_opt.py:253` deliberately left unfixed. Detail in `HANDOFF_NEXT_SESSION_2026-10-30T16-25-21Z.md`.

## Verification commands (run BEFORE declaring done)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
git status --short | grep -v __pycache__
```

## Rules (from AGENTS.md)

- Always use `SEED=42`. Never move goalposts, change tolerances/drivers/skips, or change research decisions as a side effect of verification.
- `experiments/*.json` are canonical; `run_all_verification.py` backs up and restores them — never commit verification output. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Replacing an artifact requires deliberate `scripts/check_golden_baseline.py --update` so the replacement is in the diff.
- Offline mode: `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard.
- Python 3; no separate linter — run `python3 -m py_compile` on changed files.

## Handoff outcome

Once the deterministic KKT-enumeration solver lands, the primary gate is green, and every re-pin is visible in the diff with no research conclusion changed, the session is done.
