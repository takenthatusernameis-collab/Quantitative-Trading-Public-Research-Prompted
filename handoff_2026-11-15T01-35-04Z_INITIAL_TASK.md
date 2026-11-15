# Handoff — Quantitative Trading Research

**Timestamp:** 2026-11-15T02:08:40Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Created for:** next agentic work session

## Current state
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Verification suite: `scripts/check.sh` (fast), `run_all_verification.py` (quick / extended / full).
- `experiments/*.json` are canonical golden artifacts. A verification run backs them up and restores them — never leave a run half-finished, and never commit verification output as a baseline replacement.
- `data/` parquet cache pinned in `ledger/data_baseline.json`; run verification with `QUANT_RESEARCH_OFFLINE=1`.

## Clear initial task for next session
1. Recover any interrupted verification state:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
2. Run the convention-robustness check:
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   or quick verification:
   ```bash
   SEED=42 python3 run_all_verification.py --skip-slow
   ```
3. Pick up open items from `ledger/RESEARCH_LEDGER.md` and continue validated quantitative-strategy research.

## Standing rules
- Always use `SEED=42`.
- Never commit verification output; never re-pin golden baselines as a side effect of a run (use `--update` only deliberately, which puts the replacement in the diff).
- Re-pin new data inputs with `python3 scripts/check_data_coverage.py --update` and commit the file.
