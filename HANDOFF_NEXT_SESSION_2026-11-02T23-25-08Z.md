# Initial Task Message for Next Agentic Work Session
Timestamp (UTC): 2026-11-02T23:25:08Z

## Baseline Status (resolved at write time)
- Working directory: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- Git HEAD: f4a8326 (chore(kilo): checkpoint agent session)
- Branch: main (up to date with origin/main)
- Working tree: DIRTY (12 files) — all are __pycache__/*.pyc artifacts under scripts/, src/, tests/. No source or experiment changes. Safe to ignore or clean.
- Python: /usr/bin/python3, Python 3.12.3
- Dependencies: NOT installed (ModuleNotFoundError: No module named 'pandas')

## Environment note (IMPORTANT — blocks scripts/check.sh)
Install pinned deps before running any verification:
```bash
pip install -r requirements.txt   # numpy==2.5.4 pandas==3.0.6 scipy==1.18.1 pyarrow==26.0.0 statsmodels==0.15.0 yfinance==1.7.0
```
pip may warn about user installation; use --user or a venv if needed.

## CLEAR INITIAL TASK (START HERE)
**Task:** Maintain baseline integrity and follow all project constraints. Do not run verification in a way that leaves goldens modified.

### Steps:
1. **Confirm baseline is clean before starting work:**
   - Run `SEED=42 bash scripts/check.sh` and ensure it exits 0 with "=== All checks passed ===".
   - If you see golden mismatches ("FAIL ... differ from HEAD"), recover with `git checkout -- experiments/` or `SEED=42 python3 run_all_verification.py --restore-only`. Never commit modified goldens from a verification run.
   - The backup lives in repo-local `.verify_snapshot/` (gitignored). A live run is owned by a pid marker in `ACTIVE.json`. If a stale run owns it, recover with `--restore-only`.
   - `scripts/check_goldens_clean.py` checks working tree vs HEAD; `scripts/check_golden_baseline.py` checks against SHA-256 in `ledger/golden_baseline.json`. Both must pass.
   - `scripts/check_data_coverage.py` enforces cache coverage for all data inputs (pinned in `ledger/data_baseline.json`). Unpinned inputs cause failures in offline mode.

2. **Follow project constraints:**
   - **Do not commit verification output.** If interrupted, restore goldens before committing.
   - **Golden files are canonical.** Never re-pin artifacts to silence numeric drift from verification runs. Re-pinning requires explicit justification and updating `ledger/golden_baseline.json` via `scripts/check_golden_baseline.py --update` only when appropriate.
   - **Pre-registration discipline:** Every experiment has gates/falsification expectations in pre-registered blocks. Do not move goalposts post-hoc.
   - **Multiple testing:** Sensitivity grids are "reported, not gated". Promotion requires dedicated pre-registered confirmatory run with placebo.
   - **Convention:** v1.2.3 primary is close-to-close; overnight reported alongside.
   - **Reproducibility:** Use `SEED=42`. Offline mode (`QUANT_RESEARCH_OFFLINE=1`) is used by verification.
   - **Optimizer determinism:** `src/portfolio_opt.py` validates on problem constraints, not solver exit status (SLSQP status 8 can be OK). Ill-conditioned tangency QP may show small numeric drift; do not re-pin to silence it.

3. **Current repo state notes:**
   - Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
   - Convention robustness all pass. E042 is PARTIAL (4/5 gates pass; placebo significance fails) — not promoted.
   - Extended verification shows E030/E029 now reproduce (pinned caches). E041 has reduced drift after optimizer fix but still exceeds tolerance (open item in ledger) — do not re-pin.
   - Data coverage enforced; some inputs pinned via `ledger/data_baseline.json`.
   - Latest commit: f4a8326 chore(kilo): checkpoint agent session

4. **When making changes:**
   - Understand existing patterns before editing. Follow project style (no extra comments unless asked).
   - If adding data inputs, commit files and re-pin with `python3 scripts/check_data_coverage.py --update`.
   - If tests/lint/typecheck commands are provided or standard, run them. For this repo, `python3 -m py_compile` on changed files is appropriate; `scripts/check.sh` is the main gate.
   - Never commit secrets/keys.

## Quick Start / Verify commands
- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify: `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Restore goldens if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`
- Convention robustness only: `SEED=42 python3 verify_convention_robustness.py` or `make verify`

## Suggested First Tasks
1. Run `SEED=42 bash scripts/check.sh` to confirm baseline integrity.
2. Review `ledger/RESEARCH_LEDGER.md` for open items / current state.
3. If working on experiments, follow pre-registration/falsification and multiple-testing rules.

## Handoff file map
- This file: HANDOFF_NEXT_SESSION_2026-11-02T23-25-08Z.md
- Symlinks pointing here: NEXT_HANDOFF.md, NEXT_SESSION_HANDOFF.md, handoff.md, handoff_current.md, handoff_next.md, handoff_next_session.md
- Prior session handoffs: HANDOFF_SESSION_*.md (dated 2026-10-17 through 2026-11-02), HANDOFF_NEXT_SESSION_*.md (many, in root)
- Durable state dir: handoff/ (contains HANDOFF_20261102T232041Z.md, the last substantive one)
- Research diagnostics: research_state/workflow_run_diagnostics.jsonl

(End of file)