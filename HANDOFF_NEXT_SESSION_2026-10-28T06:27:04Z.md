# HANDOFF_NEXT_SESSION_2026-10-28T06:27:04Z

**From:** current agentic session
**To:** next agentic work session
**Time (UTC):** 2026-10-28T06:27:04Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**State:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Initial Task (clear)
Verify repository integrity and be ready to act on any pending verification/ledger items without contaminating golden artifacts.

### First actions (in order)
1. **Check baseline integrity**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - Must pass cleanly. If goldens differ from HEAD or baseline pins, restore before committing:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   - `scripts/check_goldens_clean.py` reports live runs (do not kill/re-pin). `scripts/check_golden_baseline.py` enforces pinned SHAs.

2. **Read critical docs**
   - `ledger/RESEARCH_LEDGER.md` (open items, especially E041 optimizer determinism)
   - `AGENTS.md` (verification/repro rules, cache coverage, golden integrity)
   - `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`

3. **Confirm verification state**
   - If no live verification owns `.verify_snapshot/ACTIVE.json`, safe to proceed.
   - Extended verification reports go to `.verify_reports/` (gitignored).

## Known open items (do not ignore)
- **E041 (optimizer determinism):** 354→133 numeric diffs remain (ill-conditioned QP, 1-ulp sensitivity). Structural diffs fixed. Do **not** re-pin artifacts to silence; see ledger E049.
- **Extended verification drift:** E030/E041 still drift under `--extended`; E029/E030 are offline-reproducible. Tolerances unchanged.
- **Cache coverage:** Enforced via `scripts/check_data_coverage.py`. All required cache files must exist, be git-tracked, and match `ledger/data_baseline.json`. Additions require `--update` with justification.
- **CI:** Workflow cannot be created by agents; use `.github/workflow-templates/verification-gate.yml` as template.

## Constraints
- Always use `SEED=42`.
- Never modify `experiments/*.json` as a side effect of verification (suite backs up/restores).
- Never re-pin golden/data baselines casually; use `--update` only with justification and review the diff.
- Do not commit verification outputs.
- Follow multiple-testing discipline; goalposts never moved post-hoc.
- Close-to-close is v1.2.3 primary convention.

## Handoff note
If `scripts/check.sh` passes and the ledger shows no blocking tasks, the repo is in a clean verification-ready state. State readiness and await direction, or pick up any explicit ledger action.
