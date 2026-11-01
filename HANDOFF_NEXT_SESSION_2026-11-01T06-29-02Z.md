# Agentic Handoff — 2026-11-01T08:21:21Z

## Current state
- Branch `main`, up to date with `origin/main`.
- Working tree is clean except for untracked/__pycache__ bytecode changes (`.pyc` files in `scripts/`, `src/`, `tests/`). These are build artifacts; ignore or `git checkout --` them if needed.
- No uncommitted source changes.

## Last activity
- Recent commits are `chore(kilo): checkpoint agent session` checkpoints (2622dfa, 1973984, e698e8c, 2a5aff1, d44d607).
- Research phase complete (E001–E043). Validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Suggested initial task for next session
Run the convention-robustness check to confirm the tree is in a good state:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If that passes, consider running quick verification:

```bash
SEED=42 python3 run_all_verification.py --skip-slow
```

## Key conventions (from AGENTS.md)
- Always use `SEED=42`.
- `experiments/*.json` are canonical artifacts — verification overwrites then restores them; never leave a run half-finished.
- Do not commit verification output; use `run_all_verification.py --restore-only` to recover after interruption.
- Data inputs must be pinned in `ledger/data_baseline.json`; unpinned inputs are live network downloads (yfinance is not bit-reproducible). Run with `QUANT_RESEARCH_OFFLINE=1` to fail fast on missing cache.

## Files of interest
- `AGENTS.md` — full commands & conventions
- `ledger/RESEARCH_LEDGER.md` — surviving strategies & open items (incl. E049 optimizer determinism, E041/E042 drift)
- `scripts/check.sh`, `run_all_verification.py`
- `experiments/*.json` — committed golden artifacts
