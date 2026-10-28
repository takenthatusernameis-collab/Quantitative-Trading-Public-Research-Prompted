# HANDOFF - 2026-10-28T17:24:32Z

## Status
- Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- Verification infrastructure in place. `experiments/*.json` are canonical goldens.
- Baseline integrity guards active (`scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`).

## Initial Task (for next agent)
1. **Verify repo cleanliness**: Run `SEED=42 bash scripts/check.sh`. Ensure no golden mismatches, data coverage passes, and tests pass.
2. **Review open items**: Read `ledger/RESEARCH_LEDGER.md` for any open items (notably E049 optimizer determinism) and decide if action is needed.
3. **Confirm state before changes**: If verification is clean, report status. If not clean, recover with `SEED=42 python3 run_all_verification.py --restore-only` before making changes.

## Critical Rules
- Always use `SEED=42` for reproducible runs
- Never commit verification output mid-run (restore with `--restore-only` if interrupted)
- `experiments/*.json` must match `ledger/golden_baseline.json` (re-pin only with explicit justification)
- Data inputs must be committed and pinned in `ledger/data_baseline.json` (no unpinned live downloads in verification)
- Follow project conventions in `AGENTS.md`

## Key Commands
```bash
SEED=42 bash scripts/check.sh                    # fast check
SEED=42 python3 run_all_verification.py         # quick verify (~8 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens
```
