# Agentic Work Session Handoff — Initial Task Message

**Created**: 2026-11-19T10:09:47Z
**Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Repository state at creation**: HEAD `a7cbd189` == `origin/main` `a7cbd189` (0 ahead / 0 behind), working tree **not** clean — only `scripts/__pycache__/*.cpython-312.pyc` (9 tracked binary bytecode files) show as modified; no `.verify_snapshot/` exists, no interrupted verification run.

## Initial Task Message

You are continuing an independent, reproducible quantitative-research repository whose research phase is **closed** (E001–E043 experiments complete). **Do not** start new research, re-pin baselines, or change experiment artifacts unless the user explicitly asks. Orient, verify, then wait for instruction.

## Start Here (ordered)

1. **Orient**: `git log --oneline -5`, `git status --short --branch`, `git rev-parse HEAD`. Confirm HEAD matches `origin/main` and the tree is clean.
2. **Recover any interrupted verification**: if `.verify_snapshot/` exists, run `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) before doing anything else. Never commit captured verification output.
3. **Confirm golden integrity** (fast, pure-stdlib, no deps needed):
   - `python3 scripts/check_goldens_clean.py` → all committed artifacts match HEAD
   - `python3 scripts/check_golden_baseline.py` → all pinned artifacts match the baseline
   - `git diff --name-only HEAD -- experiments/` → empty
4. **Install dependencies** (this runner has python 3.12.3 but no numpy/pandas/scipy): `pip install -r requirements.txt`.
5. **Run the fast gate**: `SEED=42 bash scripts/check.sh` (≈seconds, offline).

## Working-tree note (left dirty intentionally)

Nine tracked `scripts/__pycache__/*.cpython-312.pyc` files are modified (binary content differs, sizes unchanged). They are tracked in HEAD, so `git status` is not clean. These are stale compiled bytecode from a prior session's `py_compile` run; they are **not** research artifacts and are safe to restore with `git checkout -- scripts/__pycache__/` if a clean tree is desired. Do **not** commit them as part of any checkpoint — restore instead.

## Key constraints

- Never leave a verification run half-finished. `experiments/*.json` are canonical artifacts; restoration happens via `run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- Never re-pin goldens as a side effect of running the suite. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must be explicit.
- Always use `SEED=42`.
- Do not commit verification output. Do not commit secrets/keys.
- Python 3; verify changed files with `python3 -m py_compile`. No separate linter configured.

## Useful commands

- `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — extended verification (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — full verification (~15 min)
- `SEED=42 python3 verify_convention_robustness.py` — convention robustness only
- `SEED=42 python3 run_all_verification.py --restore-only` — recover after interrupted run

## Board coordination

Check `board_read` before continuing affected work when peer context is relevant; share material findings via `board_post` (INFO/ASK/RESULT/HOLD/VETO).