# Durable Handoff — Quantitative-Trading Research

**Created:** 2026-11-21T12:56:33Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Branch:** (check with `git status` / `git branch --show-current`)

## State summary
- Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are the canonical committed research artifacts (golden baselines pinned in `ledger/golden_baseline.json`).
- Data: cached parquet in `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages). `ledger/data_baseline.json` pins SHA-256 of each driver's cache file.

## Next task
None specified yet — awaiting user instruction.

## Verification commands (run before/after any change)
- Convention-robustness check: `SEED=42 bash scripts/check.sh`  (or `make check`)
- Quick full verification (~8 min): `SEED=42 python3 run_all_verification.py` (or `make verify-quick`)
- Pin updates only when intentionally replacing a golden: `python3 scripts/check_golden_baseline.py --update` / `python3 scripts/check_data_coverage.py --update`
- Lint: `python3 -m py_compile <changed-file>`

## Critical invariants
- Never commit verification output into `experiments/`; restore goldens via `run_all_verification.py --restore-only` after an interrupted run.
- `QUANT_RESEARCH_OFFLINE=1` during verification — unpinned inputs fail hard.
- Seed: always `SEED=42`.
- Do not re-pin goldens to silence optimizer/E041 drift (ill-conditioned QP); see AGENTS.md "Optimizer determinism (ledger E049)".

## Relevant files
- `AGENTS.md` — project commands & conventions (read before running the suite)
- `src/batch_run.py`, `src/validate.py`, `src/portfolio_opt.py`
- `experiments/run_e*.py` — individual experiment drivers
- `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `scripts/check.sh`
- `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`
