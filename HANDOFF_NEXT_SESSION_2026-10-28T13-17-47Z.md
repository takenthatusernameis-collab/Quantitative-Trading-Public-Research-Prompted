# Handoff: Next Agentic Session — 2026-10-28T13:17:47Z

> **START HERE.** Repository is fully verified and stable. No new research is warranted. Your primary task is to verify stability by running the extended verification suite, confirm the pre-existing known drifts remain unchanged, and report results. Do not modify goldens, weaken tolerances, or change any gate logic. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`. All constraints below still apply.

---

## Current state (verified at handoff time)

- **HEAD:** `2b3dac2` (chore(kilo): checkpoint agent session), branch `main`, up to date with `origin/main`.
- **Working tree:** clean of tracked changes. Only `__pycache__/*.pyc` modified (gitignored; ignore them).
- **No live verification snapshot** (`.verify_snapshot/` absent, no `ACTIVE.json`). No run in progress; nothing to recover.
- **Research phase complete** (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **All guards passing** as of 2026-10-28T13:17:47Z: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `tests/test_portfolio_opt.py`, `verify_convention_robustness.py`, template validation, experiment-script imports.

## Known pre-existing drift (reporting-only; decisions unchanged)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). Three structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.

## Initial task for the next session

1. **Verify repo health (fast, offline):**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect ALL CHECKS PASSED.

2. **Run the extended verification suite (bounded, optional but recommended):**
   ```bash
   SEED=42 python3 run_all_verification.py --extended
   ```
   Expect the pre-existing E030/E041 drift above. Do **not** weaken tolerances, skip drivers, or modify committed goldens. If interrupted for any reason, recover with:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```

3. **Review open items** in `ledger/RESEARCH_LEDGER.md` (notably E049: optimizer determinism / E041 drift). Check `ledger/golden_baseline.json` and `ledger/data_baseline.json` before any intentional re-pinning.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

## Suggested first commands

```bash
git status --short
git log -1 --oneline
SEED=42 bash scripts/check.sh
```