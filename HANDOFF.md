# Session Handoff

## State
- Working tree clean except two documentation files (`README.md`, `ledger/RESEARCH_LEDGER.md`).
- Baseline checks pass: `scripts/check.sh` (ALL EXPERIMENT SCRIPT IMPORTS OK), `verify_convention_robustness.py` (ALL VERIFICATIONS PASSED).
- `SEED=42 python3 run_all_verification.py --extended` (~38 min): **23/26 drivers PASS**; the 3 FAILs (e029, e030, e041) are pre-existing numeric drift, not regressions.
- **E022 now PASSES** the extended comparison — the documented FRED placebo-z vintage-drift exception in `run_all_verification.py` is no longer triggered (`SEED=42 experiments/run_e022.py` reproduces its committed golden byte-for-byte excluding timestamp).

## What changed (this session)
- **E044: Documentation Reconciliation** — three documentation defects found and corrected against their committed artifacts. No code, no golden, no gate, no decision changed.
  1. **README E041 grid** was missing the per-component-set OOS ranges the ledger carries. Added (verified against `experiments/e041_sensitivity_grid.json`, 96 configs): all_5 0.793–1.425, equity_only_2 1.405–1.419, futures_only_2 0.357–0.672, macro_inclusive_3 0.580–0.866, cited against the grid.
  2. **README E042b artifact note** claimed `run_e042_lead.py` does NOT reproduce its golden byte-for-byte (example: OOS 0.866 -> 0.822, beta -0.001 -> +0.035, z 1.96 -> 1.64). Direct evidence contradicts this: `SEED=42 python3 experiments/run_e042_lead.py` reproduces `experiments/e042_lead_config_confirmatory.json` **byte-for-byte excluding timestamp** (only `runtime_sec` drifts: 10.9s vs ~10.6s). Corrected with the run evidence.
  3. **README "Reproducibility caveat (2026-10-17)"** claimed `run_e042.py --n-sim 50` produces 210 grid + 6592 main-golden diffs due to BLAS/LAPACK sensitivity. Direct evidence contradicts this: `SEED=42 python3 experiments/run_e042.py --n-sim 50` (~2 min) reproduces **both** `e042_minvar_market_neutral.json` and `e042_sensitivity_grid.json` **byte-for-byte excluding timestamp** — 0 diffs including the full 96-config grid. Retracted (the caveat predated the pinned 2026-10-12 vintage); decision unchanged.
- **Ledger**: added an E044 entry documenting all three corrections and an E041 "extended-verification disposition" recording the 3 pre-existing drift failures with evidence.

## Verified
- `SEED=42 bash scripts/check.sh` → ALL CHECKS PASSED.
- `SEED=42 python3 verify_convention_robustness.py` → ALL VERIFICATIONS PASSED.
- `SEED=42 python3 run_all_verification.py --extended` → 23/26 PASS (e022 now PASSes; e029/e030/e041 pre-existing drift).
- `SEED=42 python3 experiments/run_e042.py --n-sim 50` → byte-exact on both E042 goldens (evidence for defect 3).
- `SEED=42 python3 experiments/run_e042_lead.py` → byte-exact on its golden excl timestamp (evidence for defect 2).
- `git diff` contains only `README.md` and `ledger/RESEARCH_LEDGER.md` (documentation only). All committed golden JSONs restored by the suite's backup/restore; `data/` clean.

## Unresolved (documented, pre-existing)
- `run_all_verification.py --extended` e029/e030/e041 numeric drift (recorded in ledger E041 disposition). Not regressions; tolerances not weakened; no golden altered.
- CI workflow `.github/workflows/verification-gate.yml` still requires maintainer creation via GitHub UI (template at `.github/workflow-templates/verification-gate.yml`).

## Failed approaches
- Regenerating committed goldens or weakening tolerances (forbidden by goalpost discipline).
- Correcting documentation without backing it against the artifact first — all three README claims inspected were contradicted by direct artifact comparison, so each correction is now evidence-backed.

## Next precise task
No new research task is warranted (novelty search complete; all free public data sources exhausted; market-neutral portfolio line CLOSED per E041/E042/E042b). The repository is in a clean, fully-verified state. The only remaining durable action is the maintainer-gated CI workflow creation, which is outside agent scope. If a bounded in-session task is desired, the lowest-risk option is to re-run `SEED=42 python3 run_all_verification.py --extended` and confirm the 23/26 result is stable (expect the same pre-existing e029/e030/e041 drift; do not weaken tolerances or modify committed goldens).

### Constraints
- Do not modify committed golden JSONs; rely on `run_all_verification.py`'s backup/restore mechanism.
- Honor `SEED=42` and the cached 2026-10-12 parquet vintage.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).