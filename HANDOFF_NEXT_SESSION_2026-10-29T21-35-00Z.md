# Handoff — 2026-10-29T21:35:00Z

## Current State
- **Research phase complete** (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Canonical baselines**: `experiments/*.json` are golden artifacts. The verification suite backs them up before re-running and restores them afterward — never modify them as a side effect of verification.
- **Verification infrastructure**: `run_all_verification.py`, `scripts/check.sh`, `make check|verify-quick|verify-extended|verify-full`. Recovery available via `--restore-only`.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals pinned in `data/fundamentals/`. Coverage enforced by `scripts/check_data_coverage.py`.
- **Known open items**: E041 optimizer drift (ill-conditioned QP, ~133 numeric diffs) remains; do **not** re-pin to silence it. See `ledger/RESEARCH_LEDGER.md` (E049) and `tests/test_portfolio_opt.py` for optimizer determinism constraints.

## Initial Task for Next Session

**Priority 1 — Verify baseline integrity (do this first)**
1. Run convention/clean checks: `SEED=42 bash scripts/check.sh` (or `make check`).
2. If clean, run quick verification: `SEED=42 python3 run_all_verification.py` (or `make verify-quick`).
3. If interrupted at any point, recover with `SEED=42 python3 run_all_verification.py --restore-only` before committing or making changes.

**Priority 2 — Orient to open work**
1. Review `ledger/RESEARCH_LEDGER.md` for any items marked open/partial that need attention.
2. If the user specifies a new objective, follow pre-registration discipline (gates, falsification, multiple-testing) and do **not** move goalposts post-hoc.
3. Before committing any changes, ensure verification passes and `scripts/check_golden_baseline.py` remains satisfied.

## Quick Notes
- Always use `SEED=42` for reproducibility.
- Never commit verification outputs; only commit intentional research changes.
- Follow existing codebase patterns; check neighboring files/package deps before adding libraries.
- CI workflow template exists at `.github/workflow-templates/verification-gate.yml` (must be created via GitHub UI).

**Ready to proceed.** Start with Priority 1 above.
