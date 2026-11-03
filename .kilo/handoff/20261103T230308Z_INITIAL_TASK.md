# INITIAL TASK FOR NEXT AGENTIC SESSION (durable handoff)

- Created: 2026-11-03T23:03:08Z
- Repo: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- HEAD: 6fd5c499c335d71c8b2ded4107348a705b979528 (6fd5c49)
- Status: Clean tracked tree (only __pycache__ modified; experiments/ clean vs HEAD)
- Verification snapshot: none (.verify_snapshot absent)
- Experiments: 138 tracked files in experiments/
- Ledger: research complete (E001–E074); repository closed. No OPEN/PENDING/BLOCKED/TODO in ledger tail.

## Initial Task (clear, concrete)
Repository is in a clean closed state. No pending research tasks or open ledger items. The next agentic session should:

1. **Verify baseline integrity** before any changes: run `SEED=42 bash scripts/check.sh` (or `make check`). This enforces golden cleanliness, golden baseline pin, data coverage, JSON artifacts, portfolio-opt determinism, etc. All must pass.
2. **If you need to reproduce/verify experiments**, use the established commands from AGENTS.md: `make verify-quick`, `make verify-extended`, or `make verify-full`. Never leave verification half-finished (recovery: `SEED=42 python3 run_all_verification.py --restore-only`).
3. **Do not modify canonical artifacts**: `experiments/*.json` are goldens; do not re-pin without explicit justification recorded in `ledger/RESEARCH_LEDGER.md` and following the guards. Do not commit verification output.
4. **Constraints**: SEED=42 always. Follow all pre-registration/falsification/multiple-testing discipline. Respect data coverage invariants (commit any new data inputs and re-pin). Use `src/portfolio_opt.py` validation on constraints (not solver status).
5. **If no task is specified**: confirm clean state and report that the repo is closed with all experiments complete (E001–E074). No code changes needed.

## Key constraints (from AGENTS.md)
- Close-to-close v1.2.3 primary; overnight decomposition reported.
- Data cached in `data/` (gitignored except pinned vintages); fundamentals pinned in `data/fundamentals/`.
- Cache coverage enforced by `scripts/check_data_coverage.py` against `ledger/data_baseline.json`.
- Golden baseline enforced by `scripts/check_golden_baseline.py` against `ledger/golden_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see tests/test_portfolio_opt.py, ledger E049).

## Quick commands
- Check: `SEED=42 bash scripts/check.sh`
- Quick verify: `SEED=42 python3 run_all_verification.py`
- Extended: `SEED=42 python3 run_all_verification.py --extended`
- Full: `SEED=42 python3 run_all_verification.py --full`

Handoff written by agent at 2026-11-03T23:03:08Z. Durable copies in `handoff/` and `.kilo/handoff/`.
