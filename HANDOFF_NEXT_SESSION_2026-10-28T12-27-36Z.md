# Handoff: Next Agentic Session — Timestamped Initial Task

**Timestamp (UTC):** 2026-10-28T12-27-36Z
**Branch:** main
**HEAD:** 1ea007d
**Durable handoff:** HANDOFF_NEXT_SESSION_2026-10-28T12-27-36Z.md
**Working tree:** tracked  modifications only (gitignored, do not commit); verify with  M scripts/__pycache__/check_data_coverage.cpython-312.pyc
 M scripts/__pycache__/check_golden_baseline.cpython-312.pyc
 M scripts/__pycache__/check_goldens_clean.cpython-312.pyc
 M scripts/__pycache__/check_json_artifacts.cpython-312.pyc
 M scripts/__pycache__/diff_golden.cpython-312.pyc
 M src/__pycache__/cache_keys.cpython-312.pyc
 M src/__pycache__/data.cpython-312.pyc
 M src/__pycache__/offline.cpython-312.pyc
 M src/__pycache__/portfolio_opt.cpython-312.pyc
 M tests/__pycache__/test_data_coverage.cpython-312.pyc
 M tests/__pycache__/test_drift_report.cpython-312.pyc
 M tests/__pycache__/test_golden_baseline.cpython-312.pyc
 M tests/__pycache__/test_goldens_guard.cpython-312.pyc
 M tests/__pycache__/test_json_guard.cpython-312.pyc
 M tests/__pycache__/test_portfolio_opt.cpython-312.pyc
?? HANDOFF_NEXT_SESSION_2026-10-28T12-27-36Z.md.

## Initial task (do this first)

Verify baseline integrity before making any changes. This is non-negotiable.

```bash
git status --short
echo "---"
SEED=42 bash scripts/check.sh
#   or
make check
```

**Success criteria:**
- `scripts/check.sh` exits 0
- `git status --short` shows only `__pycache__/*.pyc` (gitignored) changes

**If checks fail on goldens:** restore before committing
```bash
SEED=42 python3 run_all_verification.py --restore-only
#   or
git checkout -- experiments/
```
Do **not** re-pin artifacts as a side effect of a verification run. If `HEAD` already replaced goldens, restore from the commit matching `ledger/golden_baseline.json`.

## Context

- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`. No new research is warranted unless explicitly requested.
- `experiments/*.json` (107 files) are canonical goldens; verification backs up/restores them — baseline is never modified by verification.
- Reporting-only drift (do not silence/re-pin): E041 ~133 numeric diffs (1-ulp tangency QP sensitivity), E030 numeric diffs on near-zero quantities.
- E029/E030 inputs pinned for offline reproducibility (`data/vintages.json`, `data/fundamentals/` per `data/fundamentals_vintages.json`).
- Optimizer determinism: `src/portfolio_opt.py` validates constraints (not solver exit status). `tests/test_portfolio_opt.py` enforces this.
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
- Never leave a verification run half-finished (suite backs up/restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- Ignore `__pycache__/*.pyc` — not tracked source; do not commit.
- If adding data inputs, commit them and re-pin with `python3 scripts/check_data_coverage.py --update`.

## Suggested first command

```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```
