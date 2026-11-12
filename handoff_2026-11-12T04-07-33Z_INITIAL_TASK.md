# Agentic Handoff — initial task message

**Created:** 2026-11-12T04:08:00Z
**Session:** next agentic work session

## Immediate task

Resume or continue work on the quantitative-strategy research repo. Before touching anything, run the convention check to confirm the working tree is clean:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

## Critical baseline-integrity rules (from AGENTS.md)

- `experiments/*.json` are canonical committed goldens; the verification suite overwrites them while running drivers and restores them afterwards. **Never leave a verification run half-finished.**
- If `scripts/check.sh` reports a golden mismatch, fix it **before** committing — a checkpoint commit that captures verification output silently replaces the canonical baseline.
- Never re-pin artifacts as a side effect of running the verification suite — the committed golden is the authoritative record.
- If a run is interrupted, restore before committing:
  ```bash
  SEED=42 python3 run_all_verification.py --restore-only
  # or
  git checkout -- experiments/
  ```
- `make check`, `make verify`, `make verify-full` provide local equivalents of `scripts/check.sh` / `run_all_verification.py`.

## Common commands

```bash
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # extended (~21 min)
SEED=42 python3 run_all_verification.py --full       # full (~15 min)
SEED=42 python3 run_all_verification.py --skip-slow  # convention only
SEED=42 python3 verify_convention_robustness.py      # convention only
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e042.py --n-sim 50   # min-var confirmatory
```

## Known open items

- E041 still drifts 133 numeric diffs (1-ulp QP sensitivity, ledger E049) — do not re-pin to silence.
- E042 min-var confirmatory is PARTIAL — confirmatory run with full placebo pending.

## Conventions

- Always use `SEED=42`.
- Run `python3 -m py_compile` on changed Python files (no separate linter configured).
- Do not commit verification output or secrets/keys.
