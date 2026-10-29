# Initial Task Message (Handoff) — 2026-10-29T00:08:35Z

## Context
- Repository: `Quantitative-Trading-Public-Research-Prompted`
- Research phase: **complete (E001–E043)**. Surviving validated strategies are recorded in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` (committed goldens).
- Verification guards are active: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Optimizer determinism: SLSQP `status==8` handled (E049). E041/E042 grids still show small numeric drift beyond 1e-4 tolerance (open; do **not** re-pin to silence).

## Goal for the next session
Start from a clean, verified baseline and address the highest-priority open ledger items without modifying canonical goldens.

## Concrete first steps (in order)
1. **Verify baseline integrity**
   `SEED=42 bash scripts/check.sh`
   (runs lint/compile + golden clean + golden baseline + data coverage + convention/tests)
2. **Quick reproducibility check**
   `SEED=42 make verify-quick` (or `SEED=42 python3 run_all_verification.py`)
   If interrupted/killed, recover with: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`)
3. **Review open items**
   Read `ledger/RESEARCH_LEDGER.md` (focus E048/E049). Check `ledger/golden_baseline.json` and `ledger/data_baseline.json` for current pins.
4. **Plan work**
   Only change drivers/code/tests to fix an open issue. Never re-pin goldens as a side effect of a verification run. If new data inputs are required, commit them and re-pin via `python3 scripts/check_data_coverage.py --update` (with justification in ledger).

## Hard constraints
- Always use `SEED=42`
- Never leave a verification run half-finished (use the snapshot/recovery flow)
- Do **not** commit verification output — restore goldens before committing
- Treat `experiments/*.json` as authoritative; re-pinning requires explicit intent and ledger update
- Data coverage is enforced offline where pinned; unpinned inputs will fail under `QUANT_RESEARCH_OFFLINE=1`

## Notes
- `verify-extended` reports drift in `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored). Use it for diagnostics only.
- Fundamentals for E029 are pinned in `data/fundamentals/` via `data/fundamentals_vintages.json`; E030 uses the committed 16-ETF panel.
- If `scripts/check.sh` reports a golden mismatch, fix baseline state before committing (see AGENTS.md “Baseline Integrity”).
