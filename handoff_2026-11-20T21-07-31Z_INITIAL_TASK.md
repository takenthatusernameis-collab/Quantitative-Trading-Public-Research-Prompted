# Handoff — 2026-11-20T21:09:45Z

## Initial task message for the next agentic work session

**Objective:** Continue independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043); surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## What to do first

Run the fast convention-robustness check + template validation (offline, seconds):

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If clean, run the quick verification suite (~8 min):

```bash
SEED=42 python3 run_all_verification.py
# or
make verify-quick
```

## Critical baseline integrity rules (read before running)

- `experiments/*.json` are canonical research artifacts. The verification suite overwrites them during a run and restores them afterwards — **never leave a verification run half-finished**.
- Backup lives in gitignored `.verify_snapshot/` with an `ACTIVE.json` marker holding the owning pid. A killed run stays recoverable.
- `scripts/check_goldens_clean.py` (step 0.5c) fails when a tracked artifact under `experiments/` differs from HEAD or a stale snapshot is pending. Recovery: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- `scripts/check_golden_baseline.py` (step 0.5d) compares tracked artifacts with SHA-256 pinned in `ledger/golden_baseline.json`. Replacing an artifact requires re-pinning (`python3 scripts/check_golden_baseline.py --update`). Never re-pin as a side effect of running the suite.
- Run every driver with `QUANT_RESEARCH_OFFLINE=1` — cache coverage is enforced; missing cache entries fail hard.
- **Do not commit verification output.** Restore goldens before committing.

## Known open items (ledger)

- E041 (market-neutral portfolio): REJECTED 3/5; 133 remaining numeric differences from ill-conditioned QP (1-ulp sensitivity). Decision/gate flags unchanged. Do not re-pin to silence drift. See ledger E049.
- E042 (min-var confirmatory): PARTIAL, `--n-sim 50`.
- Optimizer determinism: `src/portfolio_opt.py` validates solver answers on problem constraints, never exit status (pinned by `tests/test_portfolio_opt.py`).

## Key conventions

- Seed: always `SEED=42`.
- Close-to-close is the v1.2.3 primary convention; overnight decomposition reported alongside.
- Drivers have `pre_registered` JSON blocks; goalposts never moved post-hoc; sensitivity grids reported, not gated; negative results recorded honestly.
- Lint: `python3 -m py_compile` on changed files. No separate linter configured.

## Context

- Cache: pinned parquet vintages 2026-10-12 (`data/vintages.json`) and 2026-10-11 (committed; E026/E028/E029/E030/E034/E036/E037 request that end date). E029 fundamentals pinned separately in `data/fundamentals/` per `data/fundamentals_vintages.json`; `SEED` set makes `src/fundamentals.fetch_fundamentals()` read the snapshot.
- CI verification-gate template: `.github/workflow-templates/verification-gate.yml`; actual workflow cannot be created by automated agents (controller restores/cleans `.github/workflows/`).
