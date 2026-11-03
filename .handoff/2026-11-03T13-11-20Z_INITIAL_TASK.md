# Initial Task Message for Next Agentic Session (timestamp: 2026-11-03T13-11-20Z)

## Baseline Status (as of 2026-11-03T13:11:20Z)
- Working directory: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- Git HEAD: 780a6b5 chore(kilo): checkpoint agent session (2026-11-03)
- Branch: main
- Working tree: CLEAN (restored tracked `__pycache__/*.pyc` after a transient deletion)
- No `.verify_snapshot/` -> no interrupted verification run
- Dependencies: `pip install -r requirements.txt` was run this session (numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0, yfinance 1.7.0). `pandas` was previously missing and was the sole cause of `check.sh` failures; it is now installed in the environment.

Verify baseline before making changes:
```bash
SEED=42 bash scripts/check.sh
```
Expected: EXIT 0, "=== All checks passed ===". The "FAIL" lines in test outputs are intentional negative fixtures (malformed-artifact tests, the stale-snapshot test, the missing-manifest test).

## CLEAR INITIAL TASK (START HERE)
**Task:** Maintain baseline integrity and follow all project constraints. Do not run verification in a way that leaves goldens modified.

Steps:
1. Confirm baseline is clean before starting work:
   - Run `SEED=42 bash scripts/check.sh` and ensure it exits 0 with "=== All checks passed ===".
   - If you see golden mismatches ("FAIL ... differ from HEAD"), recover with `git checkout -- experiments/` or `SEED=42 python3 run_all_verification.py --restore-only`. Never commit modified goldens from a verification run.
   - The backup lives in repo-local `.verify_snapshot/` (gitignored). A live run is owned by a pid marker in `ACTIVE.json`. If a stale run owns it, recover with `--restore-only`.
   - `scripts/check_goldens_clean.py` checks working tree vs HEAD; `scripts/check_golden_baseline.py` checks against SHA-256 in `ledger/golden_baseline.json`. Both must pass.
   - `scripts/check_data_coverage.py` enforces cache coverage for all data inputs (pinned in `ledger/data_baseline.json`). Unpinned inputs cause failures in offline mode.
2. Follow project constraints:
   - **Do not commit verification output.** If interrupted, restore goldens before committing.
   - **Golden files are canonical.** Never re-pin artifacts to silence numeric drift from verification runs. Re-pinning requires explicit justification and updating `ledger/golden_baseline.json` via `scripts/check_golden_baseline.py --update` only when appropriate.
   - **Pre-registration discipline:** Every experiment has gates/falsification expectations in pre-registered blocks. Do not move goalposts post-hoc.
   - **Multiple testing:** Sensitivity grids are "reported, not gated". Promotion requires dedicated pre-registered confirmatory run with placebo.
   - **Convention:** v1.2.3 primary is close-to-close; overnight reported alongside.
   - **Reproducibility:** Use `SEED=42`. Offline mode (`QUANT_RESEARCH_OFFLINE=1`) is used by verification.
   - **Optimizer determinism:** `src/portfolio_opt.py` validates on problem constraints, not solver exit status (SLSQP status 8 can be OK). Ill-conditioned tangency QP may show small numeric drift; do not re-pin to silence it.
3. Current repo state notes:
   - Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
   - Convention robustness all pass. E042 is PARTIAL (4/5 gates pass; placebo significance fails) — not promoted.
   - Extended verification shows E030/E029 now reproduce (pinned caches). E041 has reduced drift after optimizer fix but still exceeds tolerance (open item in ledger) — do not re-pin.
   - Data coverage enforced; inputs pinned via `ledger/data_baseline.json`.
   - Latest commit: 780a6b5

4. When making changes:
   - Understand existing patterns before editing. Follow project style (no extra comments unless asked).
   - If adding data inputs, commit files and re-pin with `python3 scripts/check_data_coverage.py --update`.
   - If tests/lint/typecheck commands are provided or standard, run them. For this repo, `python3 -m py_compile` on changed files is appropriate; `scripts/check.sh` is the main gate.
   - Never commit secrets/keys.

**Next action:** Run `SEED=42 bash scripts/check.sh` to confirm baseline integrity. Only proceed with new work after it passes cleanly.