# Agentic Handoff — initial task message

**Created:** 2026-11-12T04:08:48Z
**Session:** next agentic work session
**Repo:** Quantitative-Trading-Public-Research-Prompted

## Immediate task

Before touching anything, confirm the working tree and baseline are clean:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If `scripts/check.sh` reports a golden mismatch under `experiments/`, fix it **before** committing — a checkpoint commit that captures verification output silently replaces the canonical baseline. Never leave a verification run half-finished; restore interrupted runs with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).

## Common commands

```bash
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # extended (~21 min)
SEED=42 python3 run_all_verification.py --full       # full (~15 min)
SEED=42 python3 verify_convention_robustness.py      # convention only
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e042.py --n-sim 50   # min-var confirmatory (PARTIAL)
```

## Critical baseline-integrity rules (from AGENTS.md)

- `experiments/*.json` are canonical committed goldens; verification overwrites them during a run and restores afterward.
- Never commit verification output; restore goldens before committing.
- Never re-pin artifacts as a side effect of running the verification suite — the committed golden is authoritative.
- `scripts/check_data_coverage.py` requires every `data.download()` call site to have a pinned cache file matching SHA-256 in `ledger/data_baseline.json`.

## Known open items

- E041 drifts 133 numeric diffs (1-ulp QP sensitivity, ledger E049) — do not re-pin to silence.
- E042 min-var confirmatory is PARTIAL — confirmatory run with full placebo pending.
- Research phase complete (E001–E043); surviving strategies in `ledger/RESEARCH_LEDGER.md`.

## Conventions

- Always use `SEED=42`.
- Run `python3 -m py_compile` on changed Python files (no separate linter configured).
- Do not commit verification output or secrets/keys.

## Handoff links

`handoff_CURRENT`, `handoff_LATEST`, `handoff_NEXT`, `handoff_INITIAL_TASK` should point to this file.
