# Handoff — 2026-11-05T20:47:41Z

## Status
Repo is in research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Committed golden artifacts live under `experiments/`; verification suite re-runs drivers then restores them — never commit verification output.

## Clear initial task for next session
Run the convention-robustness check and confirm green before any new work:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If green, the next session is clear to proceed with new experiment work. If not, fix the reported mismatch (do not re-pin goldens as a side effect) before continuing.

## Key conventions
- Always use `SEED=42`.
- Never commit secrets/keys.
- `experiments/*.json` are canonical goldens; restore via `python3 run_all_verification.py --restore-only` if a run is interrupted.
- `make check`, `make verify`, `make verify-full` are the local verification gates.
