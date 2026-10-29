# AGENTIC HANDOFF - 2026-10-29T11:36:23Z

## Session Context
- **Project:** Quantitative-Trading-Public-Research-Prompted
- **State:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baseline:** `experiments/*.json` are canonical goldens. The verification suite must never leave them half-modified.
- **Recent fixes:** Optimizer determinism (E049) resolved; data coverage enforced; E029/E030 now offline-reproducible.
- **Durable handoff:** this file was created at 2026-10-29T11:36:23Z for the next agentic work session.

## Initial Task (Priority 1)
Verify repository state is clean and ready for new work:

1. **Check golden integrity**
   ```bash
   SEED=42 python3 scripts/check_goldens_clean.py
   SEED=42 python3 scripts/check_golden_baseline.py
   ```

2. **Run fast convention checks**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   (Includes py_compile, portfolio opt tests, data coverage, convention robustness.)

3. **If checks pass:** Review `ledger/RESEARCH_LEDGER.md` for open items and propose next steps.
   **If checks fail:** Recover goldens with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) and re-verify. Do **not** re-pin baselines as a side effect of verification.

## Notes
- Always use `SEED=42` for reproducible runs.
- Data coverage is enforced; offline verification uses `QUANT_RESEARCH_OFFLINE=1`.
- Never commit verification output if a run was interrupted — restore first.
- See `AGENTS.md` for full workflows (`verify-quick`, `verify-extended`, `verify-full`).