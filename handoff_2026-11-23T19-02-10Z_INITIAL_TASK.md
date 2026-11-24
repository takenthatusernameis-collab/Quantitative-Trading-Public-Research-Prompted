# Handoff — Initial Task (2026-11-24T01:06:03Z)

## Status
Research phase complete (E001–E043). Verified drivers reproduce with 0 differences per `ledger/RESEARCH_LEDGER.md`.

## Next Task
Run the local verification gate and confirm no drift in committed golden artifacts:

```bash
SEED=42 bash scripts/check.sh
```

If `check.sh` passes, report completion. Do not commit verification output or re-pin golden files.

## Constraints
- Always use `SEED=42`.
- Never leave a verification run half-finished; restore goldens via `python3 run_all_verification.py --restore-only` if interrupted.
- Do not re-pin `experiments/*.json` or `data/` baselines as a side effect of running the suite.
