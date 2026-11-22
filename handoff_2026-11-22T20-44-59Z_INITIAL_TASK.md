# Agentic Work Session Handoff

**Created:** 2026-11-22T20:47:53Z
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Pending initial task

No specific research task was left beyond this handoff. The next session should:

1. Confirm the working tree is clean (no half-finished verification run captured driver output over goldens):
   ```bash
   SEED=42 bash scripts/check.sh
   ```
2. Re-read `AGENTS.md` for project conventions, seed (`SEED=42`), and golden-file rules.
3. Pick up the next experiment driver / research item from `ledger/RESEARCH_LEDGER.md`.
4. Run `python3 -m py_compile <file>` on any changed file before finishing.

## Key commands

- Convention robustness check: `SEED=42 bash scripts/check.sh` (or `make check`)
- Quick verification (8 drivers): `SEED=42 python3 run_all_verification.py` (or `make verify-quick`)
- Restore goldens after an interrupted run: `SEED=42 python3 run_all_verification.py --restore-only`

## Notes

- `experiments/*.json` are canonical golden artifacts — never commit verification output.
- If `check.sh` reports a golden mismatch, fix it before committing.
