# HANDOFF: Next Agentic Work Session

- **Timestamp:** 2026-10-29T06:10:04Z
- **Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- **State:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Current Git State
```bash
# Working tree has uncommitted __pycache__ changes (build artifacts)
git -C . status --short | head -15
```
- Modified: `scripts/__pycache__/*.pyc`, `src/__pycache__/*.pyc`, `tests/__pycache__/*.pyc`
- These are build artifacts - consider cleaning with `find . -name "*.pyc" -delete && find . -name "__pycache__" -type d -empty -delete` if not needed.

## INITIAL TASK (Clear & Actionable)

**Verify baseline integrity before making any changes.** The verification suite must be clean and goldens must match HEAD/baseline pins.

### Step 1: Check for stale verification snapshots
```bash
SEED=42 python3 scripts/check_goldens_clean.py
SEED=42 python3 scripts/check_golden_baseline.py
SEED=42 python3 scripts/check_data_coverage.py
```

### Step 2: Run full convention check
```bash
SEED=42 bash scripts/check.sh
```
This runs: py_compile, golden clean check, golden baseline pin check, data coverage, JSON artifact validation, convention robustness, and tests.

### Step 3: If clean, confirm verification suite passes
```bash
SEED=42 python3 run_all_verification.py --skip-slow  # or full if time permits
```

## If Issues Found

- **Stale snapshot / mid-verification:** `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`)
- **Golden mismatch vs HEAD:** Do NOT re-run verification to "fix" it. Check `ledger/golden_baseline.json` pins. If HEAD already has a bad commit, restore from the last commit with matching SHA-256 in the ledger.
- **Data coverage missing:** Add cache files and re-pin with `SEED=42 python3 scripts/check_data_coverage.py --update` (never as side-effect of verification).

## Context & Constraints

- **Goldens are canonical:** `experiments/*.json` must match committed state. Verification backs up/restores them.
- **Never leave verification half-finished:** Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker. If killed, recover with `--restore-only`.
- **Determinism notes:** E041/E042 have 1-ulp QP sensitivity (do not re-pin to silence). E029/E030 are offline-reproducible via pinned data.
- **Research complete:** Focus on maintenance/verification/integrity. New experiments require strong justification per pre-registration discipline.
- **No workflow creation:** Cannot create `.github/workflows/` (controller restores them). Use template at `.github/workflow-templates/verification-gate.yml`.

## Key Files to Review
- `AGENTS.md` - Commands, conventions, critical warnings
- `ledger/RESEARCH_LEDGER.md` - Full experiment history and decisions
- `ledger/golden_baseline.json` - Pinned golden SHAs
- `ledger/data_baseline.json` - Pinned data cache SHAs
- `run_all_verification.py` - Verification orchestrator

## Success Criteria
- [ ] `scripts/check.sh` passes with no failures
- [ ] No stale `.verify_snapshot/ACTIVE.json`
- [ ] Working tree only has intentional changes (pyc can be cleaned)
- [ ] Report status clearly to user
