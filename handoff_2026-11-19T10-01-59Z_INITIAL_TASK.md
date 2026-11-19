# Agentic Handoff — Quantitative Trading Public Research

## Session timestamp
Created: 2026-11-19T10:02:52Z

## Summary
Repo is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043); surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session
Run the convention-robustness check and verify the committed golden baselines are intact:

```
SEED=42 bash scripts/check.sh
# or
make check
```

If anything fails (especially `scripts/check_goldens_clean.py` or `scripts/check_golden_baseline.py`), fix it before committing — a checkpoint commit that captures verification output silently replaces the canonical baseline.

## Key constraints
- Never leave a verification run half-finished. `experiments/*.json` are canonical artifacts; restoration happens via `run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- Never re-pin goldens as a side effect of running the suite. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must be explicit.
- Always use `SEED=42`.
- Do not commit verification output. Do not commit secrets/keys.
- Python 3; verify changed files with `python3 -m py_compile`. No separate linter configured.

## Useful commands
- `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — extended verification (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — full verification (~15 min)
- `SEED=42 python3 verify_convention_robustness.py` — convention robustness only

## Board coordination
Check `board_read` before continuing affected work when peer context is relevant; share material findings via `board_post` (INFO/ASK/RESULT/HOLD/VETO).