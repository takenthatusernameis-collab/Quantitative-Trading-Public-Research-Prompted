# Agentic Work Handoff

**Timestamp (UTC):** 2026-11-23T05:25:55Z
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Research phase:** E001–E043 complete; surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.

## State confirmed at handoff time (this session)

The repo is in a **known-good state**. Verified read-only at 2026-11-23T05:25:55Z:

- `git status` → working tree clean (branch `main`, up to date with `origin/main`).
- `scripts/check_goldens_clean.py` → `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD`.
- `scripts/check_golden_baseline.py` → `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT`.
- `scripts/check_data_coverage.py` → `ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED`.
- `scripts/check_json_artifacts.py` → `checked 114 committed JSON artifacts / ALL COMMITTED JSON ARTIFACTS PARSE OK`.
- No stale `.verify_snapshot/` and no `.verify_reports/` present.

**Environment caveat (not a repo defect):** this sandbox has neither `pandas`
nor `numpy` installed (both are in `requirements.txt`). As a result `SEED=42 bash
scripts/check.sh` / `make check` exits 1 **only** because the guard self-tests in
`tests/test_data_coverage.py` (3 errors) and `tests/test_portfolio_opt.py` error on
the missing imports. Every real guard step exits 0 (confirmed above). The `FAIL ...
data/panel.parquet ...` / `nope.json` / fake-pid lines printed during the suite are
deliberate negative fixtures written to tempdirs by the self-tests — `data/panel.parquet`
is absent from `ledger/data_baseline.json` and from the working tree. This is documented
in `ledger/RESEARCH_LEDGER.md` (see entries around lines 7773, 8333, 9729).

## Initial task for the next session

You are starting a fresh agentic work session on this reproducible quant-research
repo. No new experiment has been authorized. Begin by re-confirming the known-good
state before touching anything:

1. **Confirm baseline integrity (read-only):**
   - `git status` and `git log --oneline -10`.
   - `SEED=42 python3 scripts/check_goldens_clean.py` and
     `SEED=42 python3 scripts/check_golden_baseline.py` — both must pass. If either
     reports a mismatch, STOP and restore the canonical goldens with
     `SEED=42 python3 run_all_verification.py --restore-only` before proceeding.
   - `SEED=42 python3 scripts/check_data_coverage.py` — confirm every `data.download()`
     call site is pinned (tracked + SHA-256 in `ledger/data_baseline.json`).
   - `SEED=42 python3 scripts/check_json_artifacts.py` — confirm all committed JSON parses.
2. **Interpret `scripts/check.sh` correctly:** if it exits 1, check *which* step failed.
   A failure isolated to `tests.test_data_coverage` / `tests.test_portfolio_opt` with
   `ModuleNotFoundError: No module named 'pandas'/'numpy'` is environment-only (install
   with `pip install -r requirements.txt` for a full end-to-end run). Any *guard* step
   failure (`check_goldens_clean`, `check_golden_baseline`, `check_data_coverage`,
   `check_json_artifacts`) is a real problem — stop and restore.
3. **Report state, then await direction.** Summarize working-tree status and any pending
   or stale `.verify_snapshot/` state. Do not start new research, edit goldens, or commit
   until a specific task is assigned.

If a task *is* already in flight (uncommitted changes, a half-finished driver), finish or
revert it cleanly rather than layering new work on top. Never leave the verification suite
half-finished — a killed run leaves driver output in place of the goldens.

## Conventions to remember

- Always use `SEED=42`.
- `experiments/*.json` are committed golden artifacts; verification drivers overwrite them
  and restore them afterwards — never commit verification output. Restoring goldens from
  `HEAD` is only safe when `HEAD` still matches `ledger/golden_baseline.json`; otherwise
  re-check out the last pinned artifact (`git checkout <commit> -- experiments/<file>`).
- Reproducibility: run with `QUANT_RESEARCH_OFFLINE=1`; all data inputs must be pinned
  (tracked + SHA-256 in `ledger/data_baseline.json`). yfinance is not bit-reproducible,
  so an unpinned input is a live download and will fail coverage.
- Lint/typecheck: run `python3 -m py_compile` on changed Python files (no separate linter
  configured). The verification suite also py_compiles drivers.
- `src/portfolio_opt.py` validates solver answers on the problem's constraints, never on the
  solver's exit status (ledger E049). Do not gate on SLSQP exit status.
- Extended reproducibility: `--extended` writes `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`
  (gitignored, outside `experiments/`). All 18 extended drivers reproduce with 0
  differences at the 2026-11-23T05:17Z measurement.
- Commit messages should match repo style; only commit when explicitly asked. Do not re-pin
  goldens to silence a tolerance violation.

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