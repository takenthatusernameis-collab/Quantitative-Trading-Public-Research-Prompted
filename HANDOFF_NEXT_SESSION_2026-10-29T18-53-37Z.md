# Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-10-29T18:53:37Z
**Status:** Initial task message (durable handoff)

## Initial Task

Run the convention-robustness check and template validation:

```bash
SEED=42 bash scripts/check.sh
```

(or `make check`). This is the fast, offline, convention-robustness gate; confirm it passes before any further work. If it reports a golden mismatch or stale snapshot, restore goldens first (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`) and re-run.

## Notes

- Research phase complete (E001–E043); surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Baseline integrity enforced by `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` (first-class steps of `check.sh`). Never re-pin golden artifacts as a side effect of running the suite.
- Use `SEED=42` for all verification runs.
