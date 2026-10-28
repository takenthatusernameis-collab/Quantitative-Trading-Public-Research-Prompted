# Handoff: Next Agentic Session — Timestamped Initial Task

**Timestamp:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Branch:** main
**HEAD:** $(git rev-parse --short HEAD) ($(git log -1 --format='%s'))
**Durable handoff:** $(basename $F)
**Working tree:** $(git status --short | wc -l) tracked changes; no `.verify_snapshot/` or `ACTIVE.json` — no interrupted verification run to recover.

## Immediate Task (do this first)

Verify baseline integrity before making any changes. This is non-negotiable.

```bash
SEED=42 bash scripts/check.sh
#   or
make check
```

This runs py_compile, convention checks, `check_goldens_clean.py`, `check_golden_baseline.py`, and `tests/test_portfolio_opt.py`.

**Success criteria:**
- `check.sh` exits 0
- `git status --short` shows only untracked/ignored files (e.g., `__pycache__/*.pyc`)

**If checks fail on goldens:** restore before committing
```bash
SEED=42 python3 run_all_verification.py --restore-only
#   or
git checkout -- experiments/
```
Do **not** re-pin artifacts as a side effect of a verification run. If `HEAD` already replaced goldens, restore from the commit matching `ledger/golden_baseline.json`.

## Context

- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` (107 files) are canonical goldens; verification backs up/restores them — baseline is never modified by verification.
- Reporting-only drift (do not silence/re-pin): E041 ~133 numeric diffs (1-ulp tangency QP sensitivity), E030 numeric diffs on near-zero quantities.
- E029/E030 inputs pinned for offline reproducibility (`data/vintages.json`, `data/fundamentals/` per `data/fundamentals_vintages.json`).
- Optimizer determinism: `src/portfolio_opt.py` validates constraints (not solver status). `tests/test_portfolio_opt.py` enforces this.
- CI workflow creation is maintainer-gated; template at `.github/workflow-templates/verification-gate.yml`.
- Cache coverage enforced by `scripts/check_data_coverage.py` against `ledger/data_baseline.json`.

## Quick Reference

- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify (~8 min): `SEED=42 python3 run_all_verification.py` (`make verify-quick`)
- Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended` (`make verify-extended`)
- Full (~15 min): `SEED=42 python3 run_all_verification.py --full` (`make verify-full`)
- Restore goldens: `SEED=42 python3 run_all_verification.py --restore-only`
- Convention robustness: `SEED=42 python3 verify_convention_robustness.py` or `make verify`

## Constraints

- Always use `SEED=42`.
- Never leave a verification run half-finished (suite backs up/restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- Ignore `__pycache__/*.pyc` — not tracked source; do not commit.
- If adding data inputs, commit them and re-pin with `python3 scripts/check_data_coverage.py --update`.

## Suggested First Command

```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```
