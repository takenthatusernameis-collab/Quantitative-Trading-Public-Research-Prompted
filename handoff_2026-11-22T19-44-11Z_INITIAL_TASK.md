# Agentic Handoff

**Created:** 2026-11-22T19:44:11Z
**Branch/HEAD:** 62f2b66d
**Working tree:** clean

## Next task

None queued. This handoff file is the initial task message for the next agentic work session.

If no new task is provided, the next session should run the convention/verification checks and confirm the tree is green:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

## Repo conventions (from AGENTS.md)

- Reproducible quantitative-strategy research on US equities/futures/macro.
- Always run with `SEED=42`.
- Experiments drivers under `experiments/*.json` are committed goldens; verification overwrites then restores them — never leave a verification run half-finished.
- `scripts/check.sh` runs convention checks incl. `check_goldens_clean.py` and `check_golden_baseline.py`.
- Lint: `python3 -m py_compile` on changed files.
- Do not commit unless explicitly asked.
