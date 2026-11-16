# Agent Handoff — 2026-11-16T09:37:45Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **Working dir**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Git state**: Working tree has modified `__pycache__/*.pyc` files (scripts/src/tests) from environment; no source changes observed. Verify before committing or stash/reset pyc noise as appropriate.

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
1. Run `SEED=42 bash scripts/check.sh` to confirm baseline/guards are clean (address pyc-only dirtiness as needed).
2. Review `ledger/RESEARCH_LEDGER.md` and open items above before any experiment or optimizer changes.
3. For any new/changed data inputs: commit cache files and re-pin with `python3 scripts/check_data_coverage.py --update`.
4. For artifact replacements: update `ledger/golden_baseline.json` via `python3 scripts/check_golden_baseline.py --update` only with explicit justification in diff/ledger.

## Key References
- `AGENTS.md` — commands, conventions, verification/baseline policy
- `ledger/RESEARCH_LEDGER.md` — research dispositions and experiment notes
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py` — optimizer determinism rules
