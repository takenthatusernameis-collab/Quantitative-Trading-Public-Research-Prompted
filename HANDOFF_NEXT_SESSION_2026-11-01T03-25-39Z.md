# Handoff (timestamp: 2026-11-01T03:25:39Z)

## INITIAL TASK (Start here)
**Goal:** Establish a clean, verified baseline before making any changes.

Execute in order:

1. [ ] **Check repo state** - Confirm clean working tree or understand modifications. `git status && git log -1 --oneline`
2. [ ] **Run fast integrity check** - `SEED=42 bash scripts/check.sh`. This runs convention robustness, template validation, and golden integrity guards.
3. [ ] **Recover if needed** - If goldens differ from HEAD or a stale snapshot is detected, run `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`). Never proceed with modified goldens.
4. [ ] **Review open items** - Read `ledger/RESEARCH_LEDGER.md` focusing on E049 (optimizer determinism), extended drift notes (E041/E042), and any other open items.
5. [ ] **Report baseline status** - Summarize pass/fail for all checks and confirm baseline is clean before taking on new work.

## Project State (verified this session)
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Golden artifacts in `experiments/*.json` are canonical. Verification backs up/restores via `.verify_snapshot/` — never leave a run half-finished.
- Pre-registration, multiple-testing discipline, and honest recording of negative results are required.
- Data coverage pinned in `ledger/data_baseline.json`; E029 fundamentals pinned in `data/fundamentals/`; E030 panel committed.
- Offline reproducibility enforced (`QUANT_RESEARCH_OFFLINE=1`) during verification.

## Baseline verification performed this session
- `git status`: clean except untracked `__pycache__/*.pyc` (bytecode only, no source changes). HEAD = `85885d0`.
- `SEED=42 bash scripts/check.sh`: **ALL VERIFICATIONS PASSED** (exit OK). Convention robustness, template validation, golden integrity guards, and all experiment script import checks green.

## Constraints
- **Do not commit verification output.** If interrupted, restore with `run_all_verification.py --restore-only` before committing.
- **Do not re-pin goldens** as a side effect of running verification. Re-pinning requires explicit justification and `--update` flags.
- **Numerical drift is expected** for ill-conditioned QP cases (E041/E042) — do not silence with re-pins. See ledger E049.
- **Use SEED=42** for all reproducibility runs.
- **CI workflow cannot be created by agents** (controller restores `.github/workflows/`). Template at `.github/workflow-templates/verification-gate.yml`.

## Quick Commands
```bash
SEED=42 bash scripts/check.sh                       # fast integrity + convention robustness
SEED=42 python3 run_all_verification.py --skip-slow # convention only fast path
SEED=42 python3 verify_convention_robustness.py     # offline, asserts recorded numbers
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens if interrupted
```

## Notes
- This is an initial-task handoff; no prior task work performed in this session.
- Working tree shows only `__pycache__/*.pyc` modifications (untracked bytecode); no source changes. HEAD = 85885d0.