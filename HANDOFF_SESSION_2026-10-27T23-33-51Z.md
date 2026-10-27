# Handoff: Session 2026-10-27T23-33-51Z
- **Timestamp:** 2026-10-27T23-33-51Z
- **Branch:** main
- **HEAD:** bfcc68f chore(kilo): checkpoint agent session
- **Previous handoff:** HANDOFF_SESSION_2026-10-27T22-40-59Z.md
- **Working tree:** Clean of tracked changes (untracked `__pycache__/*.pyc` only).

## State
- Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Verification infrastructure strict: `experiments/*.json` are canonical goldens. `run_all_verification.py` backs up/restores them. Guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Known pre-existing drift (reporting-only, decisions unchanged): E041 ~133 numeric diffs (ill-conditioned QP, optimizer determinism fixed per E049) — do **not** re-pin. E030 has numeric diffs on near-zero quantities (documented).
- Cache coverage enforced; E029/E030 inputs pinned. Extended verification may show same environment-dependent drift class.

## Initial Task (do this first)
1. **Verify repo health.**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Must pass: goldens clean vs HEAD, golden baseline fingerprint match, py_compile, `tests/test_portfolio_opt.py`, convention checks, JSON/artifact checks.

2. **Confirm clean baseline state.**
   ```bash
   git diff --name-only
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_data_coverage.py
   ```
   Expected: only `__pycache__/*.pyc` diffs (or none). Both checks must pass.

3. **Decide next action based on results.**
   - If checks pass and working tree is clean of tracked changes: no verification rerun needed. Review `ledger/RESEARCH_LEDGER.md` for open items.
   - If checks fail due to golden mismatch: restore before committing (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`). Do **not** re-pin artifacts as a side effect of a verification run.

## One Precise Next Task (bounded, optional)
No new research is warranted (novelty search complete; public data exhausted; market-neutral CLOSED per E041/E042/E042b). CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`). If desired, run `SEED=42 python3 run_all_verification.py --extended` to confirm stability — expect pre-existing E030/E041 drift; do not weaken tolerances or modify committed goldens.

## Quick Reference
- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify: `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Restore: `SEED=42 python3 run_all_verification.py --restore-only`

## Constraints
- Always use `SEED=42`
- Never leave a verification run half-finished (restores goldens)
- Do not commit verification outputs; only intentional source/data changes
- No committed-golden modification; no tolerance/driver/skip changes
- Preserve pre-registered outcomes/gates
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins)
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`)
