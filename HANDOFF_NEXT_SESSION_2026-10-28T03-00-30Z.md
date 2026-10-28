# Handoff: Next Agentic Session
- **Timestamp:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
- **Branch:** $(git branch --show-current)
- **HEAD:** $(git rev-parse HEAD)
- **Working tree:** $(git diff --name-only | wc -l) tracked changes; $(git ls-files --others --exclude-standard | wc -l) untracked files. No `.verify_snapshot/` present — no interrupted verification run to recover.

## Context
- Repo: Independent reproducible quantitative-strategy research (2014–2026 US equities/futures/macro). Research phase complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`.
- Verification infrastructure is strict: `experiments/*.json` (107 files) are canonical goldens. Never re-pin goldens as a side effect of verification. E041 (~133 numeric diffs) and E030 (documented numeric diffs) are reporting-only drift — do not re-pin to silence.
- Cache coverage enforced via `scripts/check_data_coverage.py` + `ledger/data_baseline.json`. All caches pinned per baseline.
- Open item (durable): tangency QP ill-conditioning (1-ulp moves answers) — E041/E042 grid artifacts still drift (29-133 diffs). Portfolio-construction line closed (E041/E042/E042b REJECTED/PARTIAL).

## Initial Task (do this first)
1. **Verify repo health (golden integrity).**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
2. **Confirm clean baseline state.**
   ```bash
   git diff --name-only
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_data_coverage.py
   ```
3. **Decide next action.**
   - If checks pass and working tree clean of tracked changes: no verification rerun needed. Review `ledger/RESEARCH_LEDGER.md` for open items.
   - If checks fail on goldens: restore before committing (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`). Do not re-pin artifacts as a side effect of a verification run.

## One Precise Next Task (bounded, optional)
No new research task is warranted. Repository is in a clean, fully-verified state. If a bounded in-session task is desired, tackle optimizer ill-conditioning for tangency/max_sharpe QP (`src/portfolio_opt.py`) to make E041/E042 artifacts bit-reproducible across environments, following AGENTS.md constraints (no gate changes, deliberate re-pin + ledger entry if numbers change). Otherwise re-run `SEED=42 python3 run_all_verification.py --extended` and confirm stability (expect pre-existing e030/e041 drift; do not weaken tolerances or modify committed goldens).

## Quick Reference
- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify (8 drivers): `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Restore goldens: `SEED=42 python3 run_all_verification.py --restore-only`

## Notes for Next Agent
- Always use `SEED=42`.
- Verification overwrites `experiments/*.json` temporarily — never leave a run half-finished.
- Do not commit verification outputs. Only commit intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- Bytecode files (`__pycache__/*.pyc`) are not tracked source; ignore or clean, do not commit.
- CI workflow `.github/workflows/verification-gate.yml` requires maintainer creation via GitHub UI (template at `.github/workflow-templates/verification-gate.yml`); outside agent scope.
