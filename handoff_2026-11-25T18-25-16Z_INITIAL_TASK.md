# Handoff: Next Agentic Work Session

**Created:** 2026-11-26T05:02:18Z
**Session:** checkpoint / idle handoff

## Current state

- Working tree: clean (last commit `25ae024f chore: capture completed workflow run diagnostics`).
- Research phase complete (E001–E043). Validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts live in `experiments/*.json`; never commit verification output over them.
- Verification suite backs up goldens before running and restores them after.

## Default verification commands (use SEED=42)

- `bash scripts/check.sh` — fast convention-robustness + template validation (~seconds, offline)
- `python3 run_all_verification.py` — verify-quick (~8 min)
- `python3 run_all_verification.py --extended` — verify-extended (~21 min)
- `python3 run_all_verification.py --full` — verify-full (~15 min)

## Initial task for next session

Run the convention-robustness check and confirm the tree is green before any new work:

```bash
SEED=42 bash scripts/check.sh
```

If it passes, proceed with whatever new task the user provides next. If it fails (golden mismatch or stale snapshot), recover with:

```bash
SEED=42 python3 run_all_verification.py --restore-only
```

then re-run `scripts/check.sh` before continuing.

## Guardrails

- Do not commit verification output. Restore goldens before committing (`--restore-only` or `git checkout -- experiments/`).
- Re-pinning an experiment artifact requires `python3 scripts/check_golden_baseline.py --update` and a ledger entry; never as a side effect of a verification run.
- New data inputs must be committed and re-pinned via `python3 scripts/check_data_coverage.py --update`; drivers run offline under `QUANT_RESEARCH_OFFLINE=1`.
- No new files under `.kilo/` or `.github/workflows/` unless explicitly asked (CI workflow cannot be created by automated agents; template at `.github/workflow-templates/verification-gate.yml`).
