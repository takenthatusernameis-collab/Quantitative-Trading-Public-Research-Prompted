# Handoff — 2026-10-28T13-33-07Z

## Status
- Working tree clean apart from `__pycache__` (untracked/build artifacts only).
- Board is empty; no in-flight tasks.
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Last commits visible via `git log -1 --oneline`.

## Clear initial task for next session (do first)
Run the convention/verification checks to confirm the repo is in a green state before starting any new work:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If you change any Python files, also run:
```bash
python3 -m py_compile <changed-file>
```

## Critical guardrails (from AGENTS.md)
- `experiments/*.json` are canonical goldens — **never commit verification output**.
- If a verification run is interrupted, restore goldens with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- Always use `SEED=42` for verification runs.
- Do **not** re-pin goldens as a side effect of running the verification suite. The committed baseline is authoritative.
- Data coverage is enforced: missing/pinned caches must match `ledger/data_baseline.json`. Live downloads are blocked in offline verification.
- Optimizer determinism notes apply (E049) — do not silence numeric drift by re-pinning artifacts.

## Quick context
- Full commands: see `AGENTS.md` (`make verify-quick/extended/full`, individual experiment commands)
- Ledger: `ledger/RESEARCH_LEDGER.md` (results, open items, falsification expectations)
- Baseline fingerprints: `ledger/golden_baseline.json`, `ledger/data_baseline.json`

## Suggested next actions (if green)
1. Review `ledger/RESEARCH_LEDGER.md` for any open items/TODOs.
2. Only proceed with new experiments if explicitly requested; otherwise focus on maintenance/integrity checks.
