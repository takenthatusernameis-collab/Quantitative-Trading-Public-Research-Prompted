# Agent Handoff — 2026-11-16T09:41:47Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **Working dir**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Incoming task**: Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.
- **Git state**: HEAD `a18150e5` ("chore(kilo): checkpoint agent session") on `main`; `origin/main` == HEAD; `git rev-list --left-right --count origin/main...HEAD` → `0 0` (in sync). Working tree carries only pre-existing `__pycache__/*.pyc` churn (gitignored). `.verify_snapshot/` and `.verify_reports/` absent; no interrupted verification run.

## Required Entry Checks
```bash
SEED=42 bash scripts/check.sh
# or full suite:
SEED=42 python3 run_all_verification.py          # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
```

## Baseline Integrity (critical)
- `experiments/*.json` are canonical golden artifacts. Verification overwrites then restores them — **never leave a run half-finished**.
- Stale/interrupted run recovery: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` if HEAD is clean baseline).
- If HEAD already contains captured verification output, restore pinned artifacts via `git checkout <commit> -- experiments/<file>` per `ledger/golden_baseline.json` SHA-256s.
- Golden/data guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py` (baselines in `ledger/`).
- Do **not** re-pin goldens to silence drift as a side effect of verification.

## Verified State This Session (read-only)
- `SEED=42 bash scripts/check.sh`: all standard-library guards GREEN —
  `ALL COMMITTED JSON ARTIFACTS PARSE OK` (114 artifacts),
  `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD`,
  `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT`,
  `ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED`,
  guard unit tests OK, `verify_convention_robustness.py` PASS.
- **Dependency caveat**: this sandbox lacks `numpy`/`pandas`, so `tests.test_data_coverage` (3 errors) and `tests.test_portfolio_opt` cannot run and `scripts/check.sh` exits non-zero at those steps. These are **environmental, not repository defects**. Install `pip install -r requirements.txt` first for a fully green suite.

## Known Drift / Open Items
- **E041**: optimizer determinism defect fixed (ledger E049), but ill-conditioned QP leaves ~133 numeric diffs (1-ulp sensitivity); structural diffs resolved. Extended still reports drift — **do not re-pin**.
- **E042** grid artifacts: 29–133 numeric diffs from same QP sensitivity — **do not re-pin**.
- **E029**: offline-reproducible (fundamentals pinned in `data/fundamentals/`, `data/fundamentals_vintages.json`).
- **E030**: offline-reproducible (16-ETF panel pinned in `data/`, ledger E048).

## Reproducibility & Environment
- Always `SEED=42`.
- Verification runs with `QUANT_RESEARCH_OFFLINE=1` — missing/unpinned cache inputs fail hard.
- Dependencies: `pip install -r requirements.txt` (`cvxpy`/`cvxopt` optional; optimizer falls back to scipy).

## Suggested Next Work
1. Install deps (`pip install -r requirements.txt`) so the full `SEED=42 bash scripts/check.sh` runs green; otherwise expect only the pandas/numpy-gated unit tests to error.
2. Review `ledger/RESEARCH_LEDGER.md` and the open items above before any experiment or optimizer changes.
3. For any new/changed data inputs: commit cache files and re-pin with `python3 scripts/check_data_coverage.py --update`.
4. For artifact replacements: update `ledger/golden_baseline.json` via `python3 scripts/check_golden_baseline.py --update` only with explicit justification in diff/ledger.

## Key References
- `AGENTS.md` — commands, conventions, verification/baseline policy
- `ledger/RESEARCH_LEDGER.md` — research dispositions and experiment notes
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py` — optimizer determinism rules
