# Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-17T00:05:36Z
**Repo:** `Quantitative-Trading-Public-Research-Prompted`
**Phase:** Research complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Current state
- Working tree has unstaged `__pycache__/*.pyc` modifications under `scripts/`, `src/`, and `tests/` (compiled bytecode drift only; no source changes observed). Review before committing — do not stage pyc noise.
- `experiments/*.json` are committed golden artifacts. Verification re-executes drivers, overwrites these during runs, and restores them; **never leave a run half-finished and never commit verification output**.
- Latest prior handoff: `handoff_2026-11-17T00:04:44Z_INITIAL_TASK.md`.

## Immediate tasks (in order)
1. **Restore baseline if needed:** if any golden in `experiments/` differs from HEAD or a stale `.verify_snapshot/` exists, run `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD is known-good per `ledger/golden_baseline.json`).
2. **Sanity check (fast, offline):** `SEED=42 bash scripts/check.sh` — includes goldens-clean, golden-baseline, data-coverage, JSON/template checks, and optimizer determinism tests.
3. **Quick verification:** `SEED=42 python3 run_all_verification.py --skip-slow` (or `make verify-quick`) to confirm convention/driver integrity.
4. **Extended verification (if time allows):** `SEED=42 python3 run_all_verification.py --extended` and inspect `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored, report-only) for drift.

## Known open items / invariants
- **E041:** ~133 numeric diffs remain due to 1-ulp sensitivity of an ill-conditioned QP; 3 prior structural diffs are resolved. **Do not re-pin** `experiments/*e041*` to silence drift (see ledger E049/open item).
- **E029/E030:** offline-reproducible with pinned inputs; reproduce with 0 differences (ledger E045/E048).
- **Optimizer determinism:** `src/portfolio_opt.py` must validate solutions against problem constraints, not solver exit status; pinned by `tests/test_portfolio_opt.py`.
- **Data/cache:** `QUANT_RESEARCH_OFFLINE=1` is used by the suite; all driver inputs must be pinned/tracked per `ledger/data_baseline.json` and `scripts/check_data_coverage.py`.
- **Golden baseline:** replacing any committed artifact requires explicit re-pin via `python3 scripts/check_golden_baseline.py --update` with justification in the diff/ledger — never as a side effect of verification.

## Useful commands
- `SEED=42 bash scripts/check.sh` (≈ `make check`)
- `SEED=42 python3 run_all_verification.py --skip-slow`
- `SEED=42 python3 run_all_verification.py` / `--extended` / `--full`
- `SEED=42 python3 run_all_verification.py --restore-only`
- `SEED=42 python3 scripts/check_golden_baseline.py` / `--update` (only with explicit intent)

## Blockers
- None identified. Proceed with verification/integrity checks; record any new drift or integrity findings in the ledger with evidence rather than re-pinning artifacts.
