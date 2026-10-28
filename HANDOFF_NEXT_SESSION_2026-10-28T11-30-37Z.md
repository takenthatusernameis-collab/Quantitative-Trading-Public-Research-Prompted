# Handoff: Next Agentic Session — Timestamped Initial Task

**Timestamp (UTC):** 2026-10-28T11:30:37Z
**Branch:** main
**HEAD:** 1b9956a (chore(kilo): checkpoint agent session)
**Durable handoff:** HANDOFF_NEXT_SESSION_2026-10-28T11-30-37Z.md
**Working tree:** only `__pycache__/*.pyc` modifications (gitignored); no `.verify_snapshot/` or `ACTIVE.json` — no interrupted verification run.

## Initial task (do this first)

Verify baseline integrity before making any changes.

```bash
git status --short
echo "---"
SEED=42 bash scripts/check.sh
```

**Success criteria:** `scripts/check.sh` exits 0; `git status --short` shows only `__pycache__/*.pyc`.

**If goldens fail:** restore before committing
```bash
SEED=42 python3 run_all_verification.py --restore-only
#   or
git checkout -- experiments/
```
Do not re-pin artifacts as a side effect of a verification run.

## Context

- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` (107 files) are canonical goldens; verification backs up/restores them.
- Reporting-only drift (do not silence/re-pin): E041 ~133 numeric diffs (1-ulp tangency QP sensitivity), E030 numeric diffs on near-zero quantities.
- E029/E030 inputs pinned for offline reproducibility.
- Optimizer determinism: `src/portfolio_opt.py` validates constraints (not solver exit status); `tests/test_portfolio_opt.py` enforces.
- Cache coverage enforced by `scripts/check_data_coverage.py` against `ledger/data_baseline.json`.
- CI workflow creation is maintainer-gated; template at `.github/workflow-templates/verification-gate.yml`.

## Quick reference

- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify (~8 min): `SEED=42 python3 run_all_verification.py` (`make verify-quick`)
- Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended` (`make verify-extended`)
- Restore goldens: `SEED=42 python3 run_all_verification.py --restore-only`
- Convention robustness: `SEED=42 python3 verify_convention_robustness.py` or `make verify`

## Constraints

- Always use `SEED=42`.
- Never leave a verification run half-finished.
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- Ignore `__pycache__/*.pyc` — do not commit.
- If adding data inputs, commit them and re-pin with `python3 scripts/check_data_coverage.py --update`.

## Suggested first command

```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```
