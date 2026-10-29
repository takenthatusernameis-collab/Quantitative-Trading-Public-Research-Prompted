# Durable Handoff — Initial Task Message

**Created:** 2026-10-29T00:09:30Z
**Session:** Kilo coding session
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state

No active code change in progress. The repository is a quantitative-strategy research project (2014–2026 US equities, futures, macro). Verification suite: `scripts/check.sh` (fast, offline) / `run_all_verification.py` (quick/extended/full). Committed experiment goldens live under `experiments/*.json`; do not commit verification output.

## Next task (initial)

Run the fast convention-robustness check to confirm a clean baseline:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If green, proceed to quick verification:

```bash
SEED=42 python3 run_all_verification.py
# or
make verify-quick
```

## Notes

- Never leave a verification run half-finished (it overwrites `experiments/*.json` then restores). If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Drivers run offline via `QUANT_RESEARCH_OFFLINE=1`; missing cached inputs fail hard.
- Lint: `python3 -m py_compile` on changed Python files. No separate linter configured.
