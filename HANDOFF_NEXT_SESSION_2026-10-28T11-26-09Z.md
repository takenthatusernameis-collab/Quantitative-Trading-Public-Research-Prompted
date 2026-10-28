# Handoff: Next Agentic Session — Timestamped Initial Task

**Timestamp:** 2026-10-28T11:26:09Z
**Branch:** main
**HEAD:** 7a0cdbd (chore(kilo): checkpoint agent session)
**Durable handoff:** HANDOFF_NEXT_SESSION_2026-10-28T11-26-09Z.md
**Working tree:** Clean of tracked changes; only `__pycache__/*.pyc` (gitignored). No `.verify_snapshot/` and no `ACTIVE.json` — no interrupted verification run to recover.

## Immediate Task (do this first)

Verify baseline integrity before making any changes:

```bash
SEED=42 bash scripts/check.sh
#   or
make check
```

This runs py_compile, convention checks, `check_goldens_clean.py`, `check_golden_baseline.py`, and `tests/test_portfolio_opt.py`.

If `check.sh` passes and `git status --short` shows no tracked changes: repo is stable. Review `ledger/RESEARCH_LEDGER.md` for open items; no new research is warranted unless explicitly requested.

If checks fail on goldens: restore before committing —
```bash
SEED=42 python3 run_all_verification.py --restore-only
#   or
git checkout -- experiments/
```
Do **not** re-pin artifacts as a side effect of a verification run.

## Context

- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` (107 files) are canonical goldens; never re-pin as a side effect of verification.
- Known reporting-only drift (do not silence/re-pin): E041 ~133 numeric diffs (1-ulp tangency QP sensitivity), E030 numeric diffs on near-zero quantities.
- E029/E030 inputs pinned for offline reproducibility (`data/vintages.json`, `data/fundamentals/`).
- CI workflow creation is maintainer-gated; template at `.github/workflow-templates/verification-gate.yml`.

## Quick Reference

- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify (~8 min): `SEED=42 python3 run_all_verification.py` (`make verify-quick`)
- Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended` (`make verify-extended`)
- Full (~15 min): `SEED=42 python3 run_all_verification.py --full` (`make verify-full`)
- Restore goldens: `SEED=42 python3 run_all_verification.py --restore-only`

## Constraints

- Always use `SEED=42`.
- Never leave a verification run half-finished (suite backs up/restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- Ignore `__pycache__/*.pyc` — not tracked source; do not commit.

## Suggested First Command

```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```
