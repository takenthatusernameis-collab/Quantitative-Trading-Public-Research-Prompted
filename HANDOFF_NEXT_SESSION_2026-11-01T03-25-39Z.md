# Handoff (timestamp: 2026-11-01T03:29:21Z)

## INITIAL TASK (Start here)
**Goal:** Establish a clean, verified baseline before making any changes.

Execute in order:

1. [ ] **Check repo state** - `git status && git log -1 --oneline`
2. [ ] **Run fast integrity check** - `SEED=42 bash scripts/check.sh`
3. [ ] **Recover if needed** - If goldens differ, run `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`). Never proceed with modified goldens.
4. [ ] **Review open items** - Read `ledger/RESEARCH_LEDGER.md` (E049 optimizer determinism, extended drift notes E041/E042).
5. [ ] **Report baseline status** - Summarize pass/fail and confirm baseline clean before new work.

## Project State
- Research phase complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`.
- Golden artifacts in `experiments/*.json` canonical; verification backs up/restores via `.verify_snapshot/`.
- Data coverage pinned in `ledger/data_baseline.json`; E029 fundamentals pinned; E030 panel committed.
- Offline reproducibility enforced (`QUANT_RESEARCH_OFFLINE=1`).

## Constraints
- Do not commit verification output; restore goldens if interrupted.
- Do not re-pin goldens as side effect of verification.
- Expected numerical drift for ill-conditioned QP (E041/E042) — do not silence with re-pins.
- Use SEED=42 for all reproducibility runs.
- CI workflow cannot be created by agents.

## Quick Commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --skip-slow
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py --restore-only
```

## Notes
- Initial-task handoff; no prior task work performed this session.
- HEAD = 85885d0; working tree clean except untracked __pycache__/*.pyc.
- Baseline verified this session: `SEED=42 bash scripts/check.sh` ALL VERIFICATIONS PASSED.
