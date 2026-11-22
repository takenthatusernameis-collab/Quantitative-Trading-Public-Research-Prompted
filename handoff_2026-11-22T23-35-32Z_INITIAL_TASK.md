# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-22T23:35:32Z
**Session ID**: Initial handoff created by user request (durable)
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## >>> INITIAL TASK FOR THE NEXT SESSION (do this first) <<<

1. Provision Python dependencies (this checkout has none installed):
   ```bash
   python3 -m pip install -r requirements.txt
   python3 -c "import pandas, numpy, scipy, statsmodels, yfinance; print('deps OK')"
   ```

2. Run the fast, offline baseline check and confirm it ends with `=== All checks passed ===`:
   ```bash
   SEED=42 bash scripts/check.sh
   ```

3. If green, run quick verification (~8 min) and confirm the golden artifacts reproduce:
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   The suite backs up `experiments/*.json` and restores them afterward. If it is
   ever interrupted (SIGKILL / OOM / timeout), recover with:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```

4. Review open items in `ledger/RESEARCH_LEDGER.md` before changing any golden or data
   artifact. Do **not** re-pin artifacts to silence known numeric drift.

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase COMPLETE (E001–E043). Surviving validated
strategies and negative results are documented in `ledger/RESEARCH_LEDGER.md`. All
experiments are pre-registered with falsification expectations and promotion gates.

## Key Commands

```bash
# Fast convention-robustness + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh              # or: make check

# Quick verification (~8 min; 8 experiment drivers)
SEED=42 python3 run_all_verification.py    # or: make verify-quick

# Extended verification (~21 min; quick + 18 committed drivers)
SEED=42 python3 run_all_verification.py --extended   # or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full       # or: make verify-full

# Recover goldens after an interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Current State (observed 2026-11-22T23:35Z)

- Working tree clean on `main` apart from untracked `__pycache__` build artifacts.
- **Environment gap:** Python dependencies are NOT installed (`import pandas` fails),
  so `check.sh` stops early. Fix via Initial Task step 1.
- Research phase: COMPLETE (E001–E043). No active verification run; no stale
  `.verify_snapshot/` expected (confirm with `scripts/check_goldens_clean.py`).

## Standing Cautions (do not violate)

- **Seed**: always `SEED=42` (walk-forward + placebo RNG reproducibility).
- **Golden files**: `experiments/*.json` are the committed canonical artifacts.
  Never commit verification output; `run_all_verification.py` backs up and restores them.
- **Baseline recovery**: `git checkout -- experiments/` restores whatever `HEAD` holds.
  If `HEAD` already carries a captured run, restore the pinned artifact with
  `git checkout <commit> -- experiments/<file>` where `<commit>` matches
  `ledger/golden_baseline.json`.
- **Data**: cached parquet in `data/` (gitignored except pinned vintages). Cache coverage
  is enforced by `scripts/check_data_coverage.py` against `ledger/data_baseline.json`;
  the suite runs with `QUANT_RESEARCH_OFFLINE=1`.
- **Optimizer determinism (ledger E049)**: `src/portfolio_opt.py` validates solver
  answers on the problem's constraints, never on solver exit status. E041/E042 grid
  artifacts still drift ~29–133 numeric diffs (1-ulp sensitivity). Do **not** re-pin
  them to silence drift.
- **CI gate**: cannot be created by agents. Template at
  `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real
  workflow via the GitHub UI.

## Open Items (from ledger)

- E041 optimizer drift: 133 numeric differences remain; decision/gates unchanged
  (REJECTED 3/5). Root-caused to ill-conditioned QP (E049); do not re-pin.
- E029, E030 are offline-reproducible (pinned data vintages; goldens deliberately re-pinned).
- CI workflow creation requires a human maintainer (see above).

## Handoff Mechanics (for future sessions)

This file is the durable handoff. Generic stable-alias symlinks
(`handoff_CURRENT.md`, `handoff_next.md`, `handoff_next_session.md`, `initial_task.md`,
`latest.md`, `INITIAL_TASK.md`, `LATEST.md`, `NEXT_SESSION.md`, `NEXT.md`, and their
uppercase variants) point to the newest timestamped handoff. After writing a new
`handoff_<UTC timestamp>Z_INITIAL_TASK.md`, repoint them with:
```bash
python3 scripts/repoint_handoff.py handoff_<UTC timestamp>Z_INITIAL_TASK.md
```
Timestamped historical handoffs are intentionally left untouched.
