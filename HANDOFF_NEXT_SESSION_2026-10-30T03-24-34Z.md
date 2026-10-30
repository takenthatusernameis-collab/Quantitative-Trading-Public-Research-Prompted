# Agentic Handoff | 2026-10-30T03:24:34Z

## Initial Task (start here)

Verify baseline integrity and environment readiness before making any changes.

### Required steps
1. Run guards: `SEED=42 bash scripts/check.sh` (must pass).
2. Recover if needed: check `.verify_snapshot/ACTIVE.json`; if present/stale run `SEED=42 python3 run_all_verification.py --restore-only`.
3. Confirm state: review `ledger/RESEARCH_LEDGER.md` and `ledger/golden_baseline.json`.

## Context

- Research phase complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`.
- Open follow-up: tangency QP ill-conditioning (E049). E041 (~133 diffs) and E042 (~29 diffs) grid artifacts still drift; do NOT re-pin.
- Optimizer determinism fix in place (`src/portfolio_opt.py` validates on problem constraints, not solver status; `tests/test_portfolio_opt.py` passes).
- Offline reproducibility: E029/E030 pinned; verification runs with `QUANT_RESEARCH_OFFLINE=1`.

## Constraints

- Always use `SEED=42`.
- Never leave verification half-finished; restore on interrupt.
- Do not re-pin goldens/baselines to silence drift without ledger justification.
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.

## Quick Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --extended
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e041.py
SEED=42 python3 run_all_verification.py --restore-only
```
