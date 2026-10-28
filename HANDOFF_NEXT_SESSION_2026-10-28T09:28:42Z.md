# HANDOFF_NEXT_SESSION_2026-10-28T09:28:42Z

## Initial Task (clear, do first)
1. **Establish clean baseline before any changes:**
   ```bash
   git status --short
   SEED=42 bash scripts/check.sh
   ```
   - Must pass: goldens clean vs HEAD (`scripts/check_goldens_clean.py`), `ledger/golden_baseline.json` match (`scripts/check_golden_baseline.py`), data coverage (`scripts/check_data_coverage.py`), tests.
   - Working tree is clean; HEAD `81eade7`; no `.verify_snapshot/ACTIVE.json` active.
   - If a stale snapshot or dirty goldens ever appear: `SEED=42 python3 run_all_verification.py --restore-only`. Confirm `.verify_snapshot/ACTIVE.json` removed afterward.

2. **Then pick ONE concrete focused action** — no blanket re-verify, no golden re-pinning:
   - Analysis-only from `experiments/*.json` + `ledger/RESEARCH_LEDGER.md` (safest).
   - Targeted code change: `python3 -m pytest tests/test_portfolio_opt.py -v` if touching `src/portfolio_opt.py`; never chase 1e-5 QP drift.
   - Reproduce a single experiment driver only if explicitly requested (verification restores goldens after).

## Context
- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are the committed canonical baseline; verification overwrites then restores them. Never leave a run half-finished.
- Known drift: E041 (133 numeric diffs, ill-conditioned QP, decision unchanged) and E042 — **do not re-pin** to silence. E029/E030 offline-reproducible via pinned data/fundamentals.
- CI workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml`.

## Key files
- `AGENTS.md` — commands, guards, drift/cache rules
- `ledger/RESEARCH_LEDGER.md` — REJECTED/PARTIAL/VALIDATED decisions
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `scripts/check.sh`, `run_all_verification.py`, `verify_convention_robustness.py`

## Guardrails
- Never commit verification output or overwrite canonical goldens as a side effect of verification.
- Never re-pin goldens to silence known numeric drift (E041/E042).
- Never add unpinned data downloads; commit cache files and re-pin via `python3 scripts/check_data_coverage.py --update` with rationale.
- Always use `SEED=42`; drivers run under `QUANT_RESEARCH_OFFLINE=1`.

## Timestamp
Created: 2026-10-28T09:28:42Z (UTC)
