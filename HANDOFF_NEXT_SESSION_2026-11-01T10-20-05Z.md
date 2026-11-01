# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T10:21:17Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`

## Initial Task (clear)
**Verify baseline integrity before making any changes.**

Do the following in order:

1. **Check for pending recovery** - Ensure no active verification snapshot exists. If `.verify_snapshot/ACTIVE.json` is present and stale, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
2. **Run baseline checks** - Execute `SEED=42 bash scripts/check.sh`. This runs convention robustness, template validation, golden cleanliness checks, and baseline pin checks.
3. **Read context** - Skim `ledger/RESEARCH_LEDGER.md` (pay attention to open items: E041 optimizer determinism, cache coverage enforcement) and the "Baseline Integrity" section of `AGENTS.md`.
4. **Report status** - Summarize check results. If clean, ask the user for direction (new experiment, address an open ledger item, or extend verification). If not clean, resolve golden/cache issues before proceeding.

## Hard Constraints / Reminders
- **Always use `SEED=42`** for all runs
- **Never leave verification half-finished** - the suite backs up/restores, but recovery tools exist if interrupted
- **Golden baseline is authoritative** - do not re-pin artifacts as a side effect of running verification. Re-pin only with explicit intent via `scripts/check_golden_baseline.py --update`
- **Cache coverage is enforced** - verification runs with `QUANT_RESEARCH_OFFLINE=1`. If adding data inputs, commit them and re-pin with `scripts/check_data_coverage.py --update`
- **Follow conventions** - pre-registration, multiple-testing discipline (sensitivity grids reported not gated), record negative results honestly
- **Optimizer determinism** - E041/E042 grid can drift numerically due to ill-conditioned QP; do not re-pin to silence this (see ledger E049)

## Suggested Next Action
If baseline is clean and no explicit task is provided, do **not** guess. Report status and ask for direction.