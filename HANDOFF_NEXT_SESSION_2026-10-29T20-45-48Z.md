# Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-10-29T20-45-48Z
**Status:** Initial task message (durable handoff)
**Session Owner:** Kilo (current session)
**Commit:** b5a5ae9 (chore(kilo): checkpoint agent session)

## Initial Task

**PRIMARY OBJECTIVE:** Verify repository baseline integrity and ensure clean state for continued research.

Run the fast convention-robustness gate first:

```bash
SEED=42 bash scripts/check.sh
```

(or `make check`). This validates:
- Python syntax/imports across the codebase
- Golden artifact integrity vs HEAD (`check_goldens_clean.py`)
- Golden baseline pins match (`check_golden_baseline.py`)
- Data coverage/pinning (`check_data_coverage.py`)
- Experiment template/JSON schema validation
- Portfolio optimizer regression tests

## Current State

- **Branch:** main
- **Latest commits:** checkpoint commits from current session (b5a5ae9 down to ef0582d)
- **Working tree:** Has modified `__pycache__` files (uncommitted). No changes to source, experiments, or data.
- **Research phase:** Complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- **Baselines enforced:** `ledger/golden_baseline.json`, `ledger/data_baseline.json`

## Known Issues / Important Notes

- **Pycache modifications only:** The uncommitted changes are all `__pycache__/*.pyc` files - these are build artifacts and can be safely ignored/cleaned.
- **Known reporting-only drifts (do NOT re-pin):**
  - E030: near-zero quantities (fixed by pinned panel per ledger E048)
  - E041: ~133 numeric diffs from ill-conditioned tangency QP sensitivity; optimizer determinism fixed per ledger E049. Structural diffs gone, decision unchanged (REJECTED 3/5).
- **Verification integrity:** If a previous verification was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` before running checks.

## Constraints (Must Honor)

- **Always use SEED=42** for any reproducibility
- **Never modify `experiments/*.json`** as side effect of verification - re-pinning requires `scripts/check_golden_baseline.py --update` with explicit justification
- **Honor data pins:** All cached data must be committed and pinned; verification runs offline with `QUANT_RESEARCH_OFFLINE=1`
- **Never leave verification half-finished:** Suite backs up/restores via `.verify_snapshot/` with PID tracking
- **No gate weakening:** Don't change tolerances, skip logic, or verification gates
- **No goalpost moves:** Don't alter pre-registered outcomes or validated strategy constructions
- **CI workflow:** Cannot be created by agents (maintainer-gated). Template exists at `.github/workflow-templates/verification-gate.yml`

## Quick Reference

```bash
# Fast integrity check (~seconds)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Recover interrupted run
SEED=42 python3 run_all_verification.py --restore-only

# Clean pycache if desired
find . -name "*.pyc" -delete && find . -name "__pycache__" -type d -empty -delete
```

## Key Documentation
- `AGENTS.md` - Full project conventions and commands
- `ledger/RESEARCH_LEDGER.md` - Complete experiment history and decisions
- `README.md` - Project overview

**If `scripts/check.sh` passes cleanly, the repo is in a good state for the next task. Report status and await further instructions.**
