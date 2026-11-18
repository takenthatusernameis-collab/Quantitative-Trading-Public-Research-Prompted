# Agentic Work Session Handoff

**Timestamp (UTC)**: 2026-11-18T02:40:26Z
**Session ID**: Initial handoff for next agentic work session (E479)
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch**: main
**HEAD**: 263ab0857a049ebed319520aeeb0140e5f28dcbd (== origin/main, 0 ahead / 0 behind)

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Every experiment is pre-registered with falsification
expectations and promotion gates. **Research phase is complete (E001–E051).**
Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
Durable-handoff refreshes continue the ledger; this session is **E479**.

## CLEAR INITIAL TASK (do this first)

1. **Confirm baseline integrity and a clean tree before any new work:**
   - `git status --short` → only `__pycache__/*.pyc` should be modified.
   - `git rev-parse HEAD` == `origin/main`.
   - `ls .verify_snapshot .verify_reports` → must not exist (no interrupted run).
2. **Install dependencies in this runner** (see Environment Caveat below):
   `python3 -m pip install -r requirements.txt`
3. **Run the fast gate**: `SEED=42 bash scripts/check.sh` → must end `=== All checks passed ===`.
4. Then, only if reconfirmation is wanted: `SEED=42 python3 run_all_verification.py` (verify-quick).
5. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and the open
   E041/E042 optimizer-drift disposition.
6. Do **not** re-pin golden/data baselines, modify `experiments/*.json`, or commit
   verification output as a side effect. Follow `AGENTS.md` for all conventions.

## Reproduce / Verify

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min; 8 drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; + 18 committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Recover golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Baseline Integrity (read before running the suite)

`experiments/*.json` are the canonical research artifacts. The verification suite
overwrites them while re-running drivers and restores them afterward, so **a
verification run must never be left half-finished**:

- Backup lives in repo-local, gitignored `.verify_snapshot/` with an `ACTIVE.json`
  marker holding the owning pid; a killed run stays recoverable.
- `scripts/check_goldens_clean.py` fails when a tracked artifact under
  `experiments/` differs from HEAD or a stale snapshot is pending.
- `scripts/check_golden_baseline.py` compares every tracked artifact with the
  SHA-256 fingerprint pinned in `ledger/golden_baseline.json`. Replacing an
  artifact requires re-pinning (`python3 scripts/check_golden_baseline.py --update`);
  never re-pin as a side effect of verification.
- `scripts/check_data_coverage.py` enforces that every pinned data input exists,
  is git-tracked, and matches `ledger/data_baseline.json`; unpinned inputs are
  live network downloads and yfinance is not bit-reproducible.
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only`
  (or `git checkout -- experiments/`).

## Reproducibility Notes

- **Seed**: always `SEED=42` (walk-forward + placebo RNG).
- **Convention**: close-to-close is the v1.2.3 primary convention; overnight
  decomposition is reported alongside every strategy.
- **Data**: cached parquet in `data/` (gitignored except pinned 2026-10-12 and
  2026-10-11 vintages); E029 fundamentals pinned in `data/fundamentals/`.
  Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- **Optimizer determinism (ledger E049)**: the E041/E042 grid artifacts still
  drift by ~29–133 differences due to an ill-conditioned QP (1-ulp sensitivity).
  Do **not** re-pin them to silence that.

## Current Status (as of 2026-11-18T02:40:26Z)

- HEAD `263ab085` == `origin/main` (0 ahead / 0 behind). Recent commits:
  `263ab085` (checkpoint agent session), `2e3be54e`, `7aa660f3`, `4d26f229`.
- Working tree clean apart from **12 tracked `__pycache__/*.pyc`** bytecode files
  (no source, experiment, ledger, or data changes). `experiments/` and `data/` untouched.
- No `.verify_snapshot/` or `.verify_reports/` pending.
- Verified individually this session (all exit 0):
  `check_json_artifacts.py` (114 artifacts parse OK),
  `check_goldens_clean.py` (match HEAD),
  `check_golden_baseline.py` (107/107 pinned goldens match),
  `check_data_coverage.py` (35 pinned data inputs present/tracked/unchanged).
- 107 golden artifacts under `experiments/` match `ledger/golden_baseline.json`
  and HEAD.

## Environment Caveat (important)

The `python3` on this runner (3.12.3, `/usr/bin/python3`) does **not** have the
project dependencies installed — `import pandas` raises `ModuleNotFoundError`.
Consequently:

- `SEED=42 bash scripts/check.sh` stops at `python3 -m unittest
  tests.test_data_coverage` / `tests.test_portfolio_opt` with
  `ModuleNotFoundError: No module named 'pandas'` (the earlier non-pandas steps
  still print their OK lines).
- Every non-pandas check passes when run on its own (see Current Status).
- Scheduled "Kilo General Agent Loop" runs have shown the same missing-`pandas`
  signal in job logs.

**Fix before relying on the full suite**: `python3 -m pip install -r
requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance;
`cvxpy`/`cvxopt` optional). Earlier sessions (e.g. E470) had these importable
(pandas 3.0.6), so this is a runner/image difference, not a repo regression.

## Standing Constraints

- Research phase complete (E001–E051); handoff refreshes continue the ledger (E479).
- Do not commit verification output; do not re-pin golden/data baselines unless
  the user explicitly directs it.
- This handoff is a durable artifact; leave it uncommitted unless the user asks
  to commit.

---

*Durable handoff for the next agentic work session. Mirrored to `handoff/`,
`HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` with generic alias pointers
repointed via `scripts/repoint_handoff.py`.*