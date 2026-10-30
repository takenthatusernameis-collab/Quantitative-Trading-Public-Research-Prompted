# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-10-30T23:30:00Z (UTC)
**Branch:** main
**Last commit:** `92293cc`
**Working tree:** Tracked changes limited to `__pycache__/*.pyc` (gitignored). `experiments/` may be overwritten by a stale/interrupted verification run.

---

## INITIAL TASK (do first)

1. **Recover the baseline artifacts**
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   _(Fallback: `git checkout -- experiments/`.)_

2. **Verify baseline integrity**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: `py_compile`, goldens clean vs HEAD, pinned baseline match (`ledger/golden_baseline.json`), data coverage (`ledger/data_baseline.json`), and `tests/test_portfolio_opt.py`.

3. **Do not make changes or commit without explicit user direction.**
   - Goldens are authoritative — never modify them as a side effect of verification.
   - Never re-pin to silence drift. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff.
   - Do not commit verification output. If interrupted, restore goldens before committing.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Known open item:** E041 numeric drift (133 diffs) exceeds the 1e-4 tolerance in extended verification; do **not** re-pin. E029 and E030 are offline-reproducible with 0 differences.
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver answers on the problem's constraints, not solver exit status. This is pinned by `tests/test_portfolio_opt.py`.
- **Working tree:** Only `__pycache__/*.pyc` modifications (gitignored).

---

## Immediate priorities for next session

- [ ] Recover stale snapshot if present (`SEED=42 python3 run_all_verification.py --restore-only`).
- [ ] Confirm `SEED=42 bash scripts/check.sh` passes cleanly.
- [ ] Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` before taking any action.
- [ ] Follow all project constraints: `SEED=42`, respect pre-registration and multiple-testing discipline, never commit unless explicitly asked, never modify goldens via verification.

---

## Quick reference commands

```bash
# Recover goldens after interrupted run
SEED=42 python3 run_all_verification.py --restore-only

# Full baseline integrity check
SEED=42 bash scripts/check.sh

# Fast checks (skip slow batch/regression)
SEED=42 python3 run_all_verification.py --skip-slow

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

---

## Files to read first

- `AGENTS.md` — Commands, conventions, guards, and hard constraints
- `ledger/RESEARCH_LEDGER.md` — Experiment history, decisions, and open items
- `ledger/golden_baseline.json` — Pinned SHA-256 fingerprints for `experiments/`
- `ledger/data_baseline.json` — Pinned SHA-256 fingerprints for required data inputs

---

## Notes

- Always use `SEED=42`.
- Do not commit verification output. If a run is interrupted, restore goldens before committing.
- Sensitivity grids are reported, not gated.
- CI workflow cannot be created by automated agents; template lives at `.github/workflow-templates/verification-gate.yml` with instructions in `VERIFICATION_GATE_TEMPLATE.md`.
