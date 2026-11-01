# Handoff - 2026-11-01T02:19:44Z

## Initial Task for Next Agentic Session
1. **Verify baseline integrity** (must pass before any changes):
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - Ensure no pending snapshot (check_goldens_clean.py passes)
   - Ensure goldens match ledger pins (check_golden_baseline.py passes)
   - Ensure data coverage is intact (check_data_coverage.py passes)
   - Ensure tests pass (py_compile + portfolio_opt tests)

2. **Run quick verification** to confirm reproducibility:
   ```bash
   SEED=42 make verify-quick
   ```
   (~8 min). Do not leave run interrupted - if interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

3. **Review open items** in `ledger/RESEARCH_LEDGER.md`:
   - **E049**: Optimizer determinism - E041/E042 grid artifacts still drift (133/29 numeric diffs) due to ill-conditioned QP / scipy build sensitivity. Do **NOT** re-pin goldens to silence this drift. Follow pinned rule in `src/portfolio_opt.py` and `tests/test_portfolio_opt.py`.
   - Check for any new blocks/falsifications since last session.

## Current State
- **HEAD**: 5874034 chore: capture completed workflow run diagnostics
- **Working tree**: clean (no pending snapshot, no interrupted verification run)
- **Phase**: Research complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- **Guards enforced**: golden baseline, data coverage, optimizer determinism
- **Seed**: Always use `SEED=42`
- **Offline mode**: Verification runs with `QUANT_RESEARCH_OFFLINE=1`

## Critical Reminders
- **Never re-pin goldens** as side effect of verification - only re-pin via `scripts/check_golden_baseline.py --update` with justification
- **Never commit verification output** - restore goldens if working tree is dirty from interrupted run
- **Data coverage**: Any new `data.download()` call requires committing file and re-pinning `ledger/data_baseline.json`
- **Extended verification**: `--extended` writes gitignored drift report to `.verify_reports/` only

## Quick Recovery Commands
```bash
# If goldens modified by interrupted run
SEED=42 python3 run_all_verification.py --restore-only

# Or manually
git checkout -- experiments/
```
