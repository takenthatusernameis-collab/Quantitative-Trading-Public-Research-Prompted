# Initial Task Message for Next Agentic Session (timestamp: 2026-11-02T22:19:57Z)

## Baseline Status (as of 2026-11-02T22:19:57Z)
- Working directory: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- Git HEAD: 9082937
- Branch: main
- Working tree: clean

## Environment note (IMPORTANT — blocks scripts/check.sh)
- python3 at /usr/bin/python3 (Python 3.12.3) may be missing deps. If check.sh fails with ModuleNotFoundError, install pinned deps:
  ```bash
  pip install -r requirements.txt   # numpy==2.5.4 pandas==3.0.6 scipy==1.18.1 pyarrow==26.0.0 statsmodels==0.15.0 yfinance==1.7.0
  ```
  Use --user or venv if needed.

## CLEAR INITIAL TASK (START HERE)
**Task:** Maintain baseline integrity and follow all project constraints. Do not run verification in a way that leaves goldens modified.

Steps:
1. Confirm baseline is clean before starting work:
   - Run `SEED=42 bash scripts/check.sh` and ensure it exits 0 with "=== All checks passed ===".
   - If golden mismatches appear, recover with `git checkout -- experiments/` or `SEED=42 python3 run_all_verification.py --restore-only`. Never commit modified goldens from a verification run.
   - Backup lives in repo-local `.verify_snapshot/` (gitignored). Live runs owned by pid in `ACTIVE.json`. Recover stale runs with `--restore-only`.
   - `scripts/check_goldens_clean.py` (HEAD vs working tree), `scripts/check_golden_baseline.py` (vs ledger/golden_baseline.json), and `scripts/check_data_coverage.py` must all pass.

2. Follow project constraints:
   - Do not commit verification output. Restore goldens if interrupted.
   - Golden files are canonical. Re-pinning requires explicit justification and `scripts/check_golden_baseline.py --update` (never as side effect of verification).
   - Pre-registration discipline: gates/falsification in pre-registered blocks; do not move goalposts post-hoc.
   - Multiple testing: sensitivity grids "reported, not gated"; promotion needs dedicated pre-registered confirmatory run with placebo.
   - Convention v1.2.3 primary is close-to-close; overnight reported alongside.
   - Reproducibility: use `SEED=42`. Verification uses `QUANT_RESEARCH_OFFLINE=1`.
   - Optimizer: `src/portfolio_opt.py` validates on problem constraints (SLSQP status 8 can be OK). Ill-conditioned tangency QP may drift numerically; do not re-pin to silence it.

3. Current repo state notes:
   - Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
   - Convention robustness all pass. E042 is PARTIAL (4/5 gates pass; placebo significance fails) — not promoted.
   - Extended verification: E030/E029 reproduce (pinned caches). E041 has reduced drift after optimizer fix but still exceeds tolerance (open item in ledger) — do not re-pin.
   - Data coverage enforced; inputs pinned via `ledger/data_baseline.json`.
   - Latest commit: 9082937

4. When making changes:
   - Understand existing patterns before editing. Follow project style (no extra comments unless asked).
   - If adding data inputs, commit files and re-pin with `python3 scripts/check_data_coverage.py --update`.
   - Run `python3 -m py_compile` on changed files; `scripts/check.sh` is the main gate.
   - Never commit secrets/keys.

**Next action:** Run `SEED=42 bash scripts/check.sh` to confirm baseline integrity. Only proceed with new work after it passes cleanly.
