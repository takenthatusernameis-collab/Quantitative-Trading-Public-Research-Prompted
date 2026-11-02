# AGENTIC HANDOFF - 2026-11-02T13:25:40Z

## Mission for the next session
Start by validating baseline integrity, then triage and act on the highest-priority open items in the research ledger. Do not modify canonical goldens as a side effect of verification.

## Current project state
- Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts live in `experiments/*.json`. These are goldens and must not be overwritten by verification runs.
- Verification guards are enforced: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, and `scripts/check_data_coverage.py`.
- Data coverage is enforced (`ledger/data_baseline.json`). All driver inputs must be pinned/cached; network downloads are disallowed during verification (`QUANT_RESEARCH_OFFLINE=1`).
- Optimizer determinism note (E049): `src/portfolio_opt.py` validates on problem constraints, not solver status. The tangency QP remains ill-conditioned.

## Known open/important notes
- **E041 drift**: 133 numeric diffs remain (1-ulp sensitivity of ill-conditioned QP). The 3 structural diffs are gone. Do **not** re-pin to silence this drift.
- **E029/E030**: Now offline-reproducible after pinning fundamentals/panels; goldens were deliberately re-pinned for those.
- **Verification contamination risk**: If a run was interrupted, `experiments/` may hold driver outputs instead of goldens. Always restore before committing.

## First actions (in order)
1. **Inspect repo state**
   ```bash
   git status && git log --oneline -3
   ```
2. **Validate baseline integrity (fast)**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   If this reports a golden mismatch and you're not intentionally updating baselines, restore first.
3. **Recover if needed**
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   (or `git checkout -- experiments/` if appropriate; prefer the pinned commit if HEAD already captured a run).
4. **Triage open work**
   - Read `ledger/RESEARCH_LEDGER.md` end-to-end for open items and their priority.
   - Review `ledger/golden_baseline.json` and `ledger/data_baseline.json` to understand what is pinned.
   - Propose a concrete next task based on the ledger (do not start broad refactors without a specific, ledger-backed objective).

## Verification commands (reference)
- Fast: `SEED=42 bash scripts/check.sh` or `make check`
- Quick full: `SEED=42 python3 run_all_verification.py` or `make verify-quick` (~8 min)
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended` (~21 min)
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full` (~15 min)
- Convention only: `SEED=42 python3 verify_convention_robustness.py` or `make verify`

## Hard constraints
- Always use `SEED=42`.
- Never re-pin goldens as a side effect of running the verification suite. To intentionally update a baseline, use `python3 scripts/check_golden_baseline.py --update` with justification and only if the change is correct.
- Never commit verification output. Restore goldens before committing if they're contaminated.
- All data must remain coverage-compliant. To add inputs, commit them and re-pin with `python3 scripts/check_data_coverage.py --update`.
- Do not move goalposts post-hoc. Follow pre-registered gates and multiple-testing discipline (sensitivity grids are reported, not gated).

## Key files to read first
- `AGENTS.md` (commands, guards, conventions)
- `ledger/RESEARCH_LEDGER.md` (source of truth for open items)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `scripts/check.sh`, `run_all_verification.py`
