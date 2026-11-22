# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-22T23-32-44Z
**Session ID**: Initial handoff (durable, user-requested)
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase complete (E001–E043). Surviving validated
strategies and every negative result are documented in `ledger/RESEARCH_LEDGER.md`.
All experiments are pre-registered with falsification expectations and promotion gates.

## >>> INITIAL TASK FOR THE NEXT SESSION (do this first) <<<

1. Provision Python dependencies (this checkout has none installed):
   ```bash
   python3 -m pip install -r requirements.txt
   ```
   Confirm `python3 -c "import pandas, numpy, scipy, statsmodels"` succeeds.
2. Run the fast, offline baseline check and confirm it ends with `=== All checks passed ===`:
   ```bash
   SEED=42 bash scripts/check.sh
   ```
3. If green, run the quick verification (~8 min) and confirm the golden artifacts
   reproduce:
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   The suite backs up `experiments/*.json` and restores them afterward. If it is ever
   interrupted (SIGKILL / OOM / timeout), recover with:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
4. Before changing any golden or data artifact, read the standing cautions below and
   the open items in `ledger/RESEARCH_LEDGER.md`. Do **not** re-pin artifacts to
   silence known numeric drift.

## Key Commands

```bash
# Fast convention-robustness + template validation (~seconds, offline; reads JSONs, no writes)
SEED=42 bash scripts/check.sh            # or: make check

# Quick verification (~8 min; 8 experiment drivers)
SEED=42 python3 run_all_verification.py  # or: make verify-quick

# Extended verification (~21 min; quick + 18 committed drivers)
SEED=42 python3 run_all_verification.py --extended   # or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full       # or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py      # or: make verify

# Recover goldens after an interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Current State (observed 2026-11-22T23:31Z)

- Working tree clean; `git status` empty on `main`.
- Baseline integrity checks that PASS: `check_json_artifacts.py`,
  `check_goldens_clean.py` (artifacts match HEAD), `check_golden_baseline.py`
  (107 pinned goldens match fingerprint), `check_data_coverage.py` (exit 0;
  35 pinned data inputs present/tracked).
- **Environment gap (the reason `check.sh` currently errors):** Python dependencies
  are NOT installed in this checkout. `import pandas` fails, so
  `tests/test_portfolio_opt` reports `ModuleNotFoundError: No module named 'pandas'`
  (3 errors) and `check.sh` (which runs `set -e`) stops there. This is an
  environment-provisioning issue, not a research-artifact problem.
- The `FAIL experiments/<x>.json ...` and `FAIL data/panel.parquet ...` lines seen in
  `check.sh` output are EXPECTED: they come from the guard unit tests
  (`tests.test_json_guard`, `tests.test_data_coverage`, etc.) deliberately feeding
  malformed fixtures / temp dirs to prove the guards reject them. Those suites report
  `OK` — do not "fix" them.
- Research phase: COMPLETE (E001–E043). No active verification run; no stale
  `.verify_snapshot/` expected (verify with `scripts/check_goldens_clean.py`).

## Standing Cautions (do not violate)

- **Seed**: always `SEED=42` (walk-forward + placebo RNG reproducibility).
- **Golden files**: `experiments/*.json` are the committed canonical artifacts. Never
  commit verification output. `run_all_verification.py` backs them up and restores them.
- **Baseline recovery**: `git checkout -- experiments/` restores whatever `HEAD` holds.
  If `HEAD` already carries a captured run, restore the pinned artifact instead with
  `git checkout <commit> -- experiments/<file>`, where `<commit>` is the last one whose
  SHA-256 matches `ledger/golden_baseline.json`.
- **Data**: cached parquet in `data/` (gitignored except pinned vintages). Cache coverage
  is enforced by `scripts/check_data_coverage.py` against `ledger/data_baseline.json`;
  the suite runs with `QUANT_RESEARCH_OFFLINE=1`. To add an input, commit it and re-pin:
  `python3 scripts/check_data_coverage.py --update`.
- **Optimizer determinism (ledger E049)**: `src/portfolio_opt.py` validates solver
  answers on the problem's constraints, never on the solver exit status. The tangency QP
  is ill-conditioned: E041/E042 grid artifacts still drift by ~29–133 numeric diffs
  (1-ulp sensitivity). Do **not** re-pin them to silence the drift.
- **CI gate**: cannot be created by agents. Template at
  `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real
  workflow via the GitHub UI.

## Open Items (from ledger)

- E041 optimizer drift: 133 numeric differences remain; decision/gates unchanged
  (REJECTED 3/5). Root-caused to ill-conditioned QP (E049); do not re-pin.
- E029, E030 are offline-reproducible (pinned data vintages; goldens deliberately re-pinned).
- CI workflow creation requires a human maintainer (see above).

## Handoff Mechanics (for future sessions)

This file is the durable handoff. Generic stable-alias symlinks (e.g. `handoff_CURRENT.md`,
`next_session.md`, `initial_task.md`, and their copies under `handoff/` and `HANDOFFS/`)
point to the newest timestamped handoff. After writing a new
`handoff_<UTC timestamp>Z_INITIAL_TASK.md`, repoint them with:
```bash
python3 scripts/repoint_handoff.py handoff_<UTC timestamp>Z_INITIAL_TASK.md
```
Timestamped historical handoffs are intentionally left untouched.