# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-29T23:53:15Z (message time)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `8e2af23` (working tree clean of tracked changes; only `__pycache__/*.pyc`, gitignored; no `.verify_snapshot/` active; no interrupted run to recover).

## Initial Task (Start Here)

Verify the baseline is clean before any work.

1. Run `SEED=42 bash scripts/check.sh` — all guards must pass with no golden diffs.
2. Run `git status --short` / `git diff --name-only` — confirm clean tree (only `__pycache__/*.pyc`, gitignored).
3. If an interrupted verification left dirty `experiments/*.json`, restore:
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).

Do not re-pin goldens to silence drift. Keep committed goldens authoritative.
Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` first.

## Constraints

- Always use `SEED=42`.
- Never leave a verification run half-finished.
- Do not commit verification outputs; only intentional source/data changes.

## Quick Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
```
