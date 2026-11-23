# Agentic Work Handoff

**Timestamp (UTC):** 2026-11-23T05-24-31Z
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Research phase:** E001–E043 complete; surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Initial task for the next session

You are starting a fresh agentic work session on this reproducible quant-research
repo. No new experiment has been authorized, so begin by establishing a known-good
state before touching anything:

1. **Confirm baseline integrity first (read-only):**
   - `git status` and `git log --oneline -10` to see the current working tree.
   - `SEED=42 python3 scripts/check_goldens_clean.py` and
     `SEED=42 python3 scripts/check_golden_baseline.py` — both must pass. If either
     reports a mismatch, STOP and restore the canonical goldens with
     `SEED=42 python3 run_all_verification.py --restore-only` before proceeding.
   - `SEED=42 python3 scripts/check_data_coverage.py` — confirm every `data.download()`
     call site is pinned (tracked + SHA-256 in `ledger/data_baseline.json`).
2. **Run the fast gate:** `SEED=42 bash scripts/check.sh` (or `make check`). It should
   pass in seconds, fully offline.
3. **Report state, then await direction.** Once the gate is green, summarize the
   working-tree status and any pending/stale `.verify_snapshot/` state. Do not start
   new research, edit goldens, or commit until a specific task is assigned.

If a task *is* already in flight (uncommitted changes, a half-finished driver), finish
or revert it cleanly rather than layering new work on top. Never leave the verification
suite half-finished — a killed run leaves driver output in place of the goldens.

## Conventions to remember

- Always use `SEED=42`.
- `experiments/*.json` are committed golden artifacts; verification drivers overwrite
  them and restore them afterwards — never commit verification output. Restoring goldens
  from `HEAD` is only safe when `HEAD` still matches `ledger/golden_baseline.json`;
  otherwise re-check out the last pinned artifact
  (`git checkout <commit> -- experiments/<file>`).
- Reproducibility: run with `QUANT_RESEARCH_OFFLINE=1`; all data inputs must be pinned
  (tracked + SHA-256 in `ledger/data_baseline.json`). yfinance is not bit-reproducible,
  so an unpinned input is a live download and will fail coverage.
- Lint/typecheck: run `python3 -m py_compile` on changed Python files (no separate
  linter configured). The verification suite also py_compiles drivers.
- `src/portfolio_opt.py` validates solver answers on the problem's constraints, never on
  the solver's exit status (ledger E049). Do not gate on SLSQP exit status.
- Extended reproducibility: `--extended` writes `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`
  (gitignored, outside `experiments/`). All 18 extended drivers reproduce with 0
  differences at the 2026-11-23T05:17Z measurement.
- Commit messages should match repo style; only commit when explicitly asked. Do not
  re-pin goldens to silence a tolerance violation.

## Key commands

- `make check` = `SEED=42 bash scripts/check.sh` — fast convention-robustness + template check.
- `make verify-quick` — re-executes the 8 drivers in block 5a and compares to goldens.
- `make verify-extended` — additionally re-executes the remaining 18 committed drivers.
- `make verify-full` — E042 n_sim=50 + 96-config sensitivity grid.
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only`.

## Board

Use `board_post`/`board_read` for peer coordination when multiple agents are involved.
This session's row is flagged self: true; do not post to yourself. Share material
findings (baseline mismatches, stale snapshots, blockers) rather than routine progress.