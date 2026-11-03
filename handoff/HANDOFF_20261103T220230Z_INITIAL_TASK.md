# Durable Handoff — Initial Task Message

## Timestamp
Created: 2026-11-03T22:12:06Z

## Session context
Branch: `main` (up to date with `origin/main`). Working tree is clean except for `__pycache__/*.pyc` bytecode files (untracked changes only; no source modifications pending).

## Repo state
Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. Committed experiment artifacts live in `experiments/*.json` and must never be overwritten by verification output.

## Immediate next task
Re-run the convention-robustness + golden-baseline check:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

This runs `py_compile`, `check_goldens_clean.py` (working tree vs HEAD), `check_golden_baseline.py` (tracked artifacts vs `ledger/golden_baseline.json` SHA-256 pins), `check_data_coverage.py` (all `data.download()` inputs pinned and git-tracked), and the test suite. It must pass green before any commit.

## If the check reports a golden mismatch
Fix it before committing. Do **not** let a verification run capture output into `experiments/`. If a run was interrupted and `experiments/` holds driver output instead of goldens, restore first:

```bash
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

Then re-pin only through `python3 scripts/check_golden_baseline.py --update` (puts the replacement in the diff) — never as a side effect of running the suite.

## Key conventions to honor
- Always run with `SEED=42`.
- `QUANT_RESEARCH_OFFLINE=1` is used by the suite; missing cache entries fail hard.
- Never commit secrets/keys; never add comments to code unless asked.
- Do not commit unless explicitly requested.

## Open items / notes
- `src/portfolio_opt.py`: SLSQP status-8 "Positive directional derivative for linesearch" at a constrained optimum is accepted (feasible, optimal point) — see `tests/test_portfolio_opt.py` and ledger E049.
- E041 still drifts 133 numeric differences (1-ulp QP sensitivity) — do **not** re-pin to silence it; see ledger open item.
- CI verification-gate workflow template: `.github/workflow-templates/verification-gate.yml`; a maintainer must create the actual workflow via GitHub UI (agents cannot).

## Board
Shared board is empty; no pending peer messages.
