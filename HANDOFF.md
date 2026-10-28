# HANDOFF - 2026-10-28T11:29:11Z

## Initial task for next agentic session
- **Goal:** Verify repository state and ensure baseline integrity before any new experiments.
- **Context:** Research phase complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`. All experiments are pre-registered with falsification expectations and promotion gates.
- **First checks (required):**
  1. Run `SEED=42 bash scripts/check.sh` to validate conventions and golden baseline integrity.
  2. If `scripts/check_goldens_clean.py` or `scripts/check_golden_baseline.py` report issues, restore goldens before committing (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` as appropriate).
  3. Confirm `ledger/golden_baseline.json` matches current tracked `experiments/*.json` SHAs.
- **Notes:**
  - Never modify `experiments/*.json` as a side effect of verification runs; suite backs up/restores.
  - Cache coverage is enforced (`scripts/check_data_coverage.py`) - missing/pinned inputs are required.
  - Follow AGENTS.md conventions strictly (seeds, pre-registration, multiple-testing discipline).
- **Next steps:** Report any baseline drift/failures and proceed per user priorities only after clean baseline.