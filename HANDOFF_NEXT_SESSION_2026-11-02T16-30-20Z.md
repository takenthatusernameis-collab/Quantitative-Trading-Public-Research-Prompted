# HANDOFF - Next Agentic Session
Timestamp: 2026-11-02T16:30:20Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch/HEAD: 6e3bea6 (chore(kilo): checkpoint agent session)

## Initial Task (Clear & Actionable)
**PRIMARY OBJECTIVE:** Verify repository baseline integrity and confirm verification suite is healthy before making any code changes. Do not modify experiments/ goldens or re-pin baselines as a side effect of running verification.

## Current State
- Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Recent commits are kilo checkpoints (no source changes).
- Handoffs managed via symlinks in `.kilo/` pointing to timestamped files in repo root.

## Immediate Checks (Do First)
1. **Golden baseline integrity**
   ```bash
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_goldens_clean.py
   ```
   - Must pass. If either fails, restore from HEAD or pinned commit before committing.

2. **Data/cache coverage**
   ```bash
   python3 scripts/check_data_coverage.py
   ```
   - Every driver data dependency must exist, be tracked, and match `ledger/data_baseline.json`. Missing cache = hard failure under offline verification.

3. **Quick sanity (fast)**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - Runs py_compile, convention robustness, goldens clean/baseline, data coverage, portfolio opt tests.

## Verification (If Needed)
- Quick: `SEED=42 python3 run_all_verification.py` (~8 min)
- Extended: `SEED=42 python3 run_all_verification.py --extended` (~21 min) - checks 18 more drivers
- Full: `SEED=42 python3 run_all_verification.py --full` (~15 min) - E042 n_sim=50 + 96-config grid
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` if interrupted

**Critical:** Never leave verification half-finished. Backup lives in `.verify_snapshot/` with `ACTIVE.json`. Suite self-recovers/refuses concurrent runs.

## Known Gotchas
- **Goldens**: `experiments/*.json` are canonical. Verification backs up and restores them. Never re-pin to silence drift.
- **Optimizer determinism (E049)**: SLSQP status 8 is environment-dependent but solver can be optimal/feasible. Validation is on problem constraints. E041/E042 may show bounded numeric drift (ill-conditioned QP) - do not re-pin.
- **Data pins**: E029 fundamentals pinned in `data/fundamentals/`; E030 panel committed; vintages in `data/vintages.json`.
- **CI workflow**: Cannot be created by agents (controller restores `.github/workflows/`, token lacks permission). Template at `.github/workflow-templates/verification-gate.yml`.

## Suggested Next Actions
- [ ] Run `SEED=42 bash scripts/check.sh` and report results
- [ ] If clean, proceed with user's next request. If failures, restore goldens/data before any changes.
- [ ] Keep all changes minimal and follow project conventions (SEED=42, close-to-close primary, pre-registration gates).

## Notes
- Use `SEED=42` for all runs
- Close-to-close is v1.2.3 primary convention; overnight decomposition reported
- Do not commit verification outputs
