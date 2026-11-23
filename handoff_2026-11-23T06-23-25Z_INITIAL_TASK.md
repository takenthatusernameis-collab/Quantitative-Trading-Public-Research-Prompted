# Agentic Work Session Handoff — Initial Task

**Timestamp (UTC):** 2026-11-23T06:23:25Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Research phase:** E001–E043 complete; surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Purpose of this handoff

This is the durable starting point for the next agentic work session. Read this
file first, re-confirm the known-good state, then await a specific task. No new
experiment has been authorized.

## State at handoff time

- Branch `main`, up to date with `origin/main`.
- Working tree clean except one benign tracked bytecode artifact
  (`src/__pycache__/cache_keys.cpython-312.pyc`) — a compile cache, not a source
  change. Do not commit it as part of any handoff bookkeeping.
- Golden artifacts in `experiments/*.json` are the canonical baselines; never
  commit verification output over them.

## Initial task for the next session

1. **Confirm baseline integrity (read-only) before touching anything:**
   - `git status` and `git log --oneline -10`.
   - `SEED=42 python3 scripts/check_goldens_clean.py` — every tracked artifact
     under `experiments/` must match HEAD.
   - `SEED=42 python3 scripts/check_golden_baseline.py` — every artifact must
     match the SHA-256 pinned in `ledger/golden_baseline.json`.
   - `SEED=42 python3 scripts/check_data_coverage.py` — every `data.download()`
     call site must be pinned (tracked + SHA-256 in `ledger/data_baseline.json`).
   - `SEED=42 python3 scripts/check_json_artifacts.py` — all committed JSON parses.
   - If any guard fails, STOP and restore with
     `SEED=42 python3 run_all_verification.py --restore-only` before proceeding.
     If a mismatch is a *commit* that replaced the baseline (invisible to
     `check_goldens_clean.py`), restore the last pinned artifact with
     `git checkout <commit> -- experiments/<file>` where `<commit>` is the last
     one whose SHA-256 matches `ledger/golden_baseline.json`.
2. **Interpret `scripts/check.sh` correctly.** If it exits 1, check *which* step
   failed. A failure isolated to `tests.test_data_coverage` /
   `tests.test_portfolio_opt` with `ModuleNotFoundError: No module named
   'pandas'/'numpy'` is environment-only — install with
   `pip install -r requirements.txt` for a full end-to-end run. Any *guard* step
   failure is a real problem: stop and restore.
3. **Report state, then await direction.** Summarize working-tree status and any
   stale `.verify_snapshot/` / `.verify_reports/` state. Do not start new
   research, edit goldens, or commit until a specific task is assigned.

If a task is already in flight (uncommitted changes, a half-finished driver),
finish or revert it cleanly rather than layering new work on top. Never leave the
verification suite half-finished — a killed run leaves driver output in place of
the goldens (recoverable via the repo-local `.verify_snapshot/` with an
`ACTIVE.json` marker).

## Verification commands available

```bash
# Fast convention-robustness + template check (~seconds, offline)
SEED=42 bash scripts/check.sh        # or: make check

# Quick full verification (~8 min; 8 experiment drivers)
SEED=42 python3 run_all_verification.py            # or: make verify-quick

# Extended verification (~21 min; +18 committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended # or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full     # or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py    # or: make verify

# Recover goldens after an interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Conventions to remember

- Always use `SEED=42`. Walk-forward + placebo RNG depend on it.
- `experiments/*.json` are committed golden artifacts; verification drivers
  overwrite them and restore afterwards. Never commit verification output.
- Reproducibility: run with `QUANT_RESEARCH_OFFLINE=1`; all data inputs must be
  pinned (tracked + SHA-256 in `ledger/data_baseline.json`). yfinance is not
  bit-reproducible, so an unpinned input is a live download and fails coverage.
- Reproducibility baseline: all 18 extended drivers reproduced with 0
  differences at the 2026-11-23T05:17Z measurement (numpy 2.5.4, scipy 1.18.1).
- Do NOT re-pin E041/E042 goldens to silence a tolerance violation — there is no
  remaining violation. Re-pin only for a deliberate code change that alters a
  published number, and record it in the ledger first (see the E050 precedent).
- `src/portfolio_opt.py` validates solver answers on the problem's constraints,
  never on the solver's exit status (ledger E049). Do not gate on SLSQP exit
  status.
- Lint/typecheck: run `python3 -m py_compile` on changed Python files (no
  separate linter configured). The verification suite also py_compiles drivers.
- Pre-registration: never move goalposts post-hoc. Sensitivity grids are
  "reported, not gated." Negative results are recorded honestly.
- Commit messages should match repo style; only commit when explicitly asked.

## Board

Use `board_post`/`board_read` for peer coordination when multiple agents are
involved. Your own row is flagged self: true — do not post to yourself. Share
material findings (baseline mismatches, stale snapshots, blockers) rather than
routine progress.
