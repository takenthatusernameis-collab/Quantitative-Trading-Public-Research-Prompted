# Durable Handoff — Initial Task Message

**Created:** 2026-10-29T02:09:25Z
**Session:** Kilo coding session
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state

No active code change in progress. Repository is a quantitative-strategy research project (2014–2026 US equities, futures, macro). Verification suite: `scripts/check.sh` (fast, offline) / `run_all_verification.py` (quick/extended/full). Committed experiment goldens live under `experiments/*.json`; do not commit verification output.

## Next task (initial)

No specific objective assigned. Establish a clean baseline before any changes:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If green, proceed only when a concrete objective is provided. Then read relevant drivers/tests, make minimal changes, run `python3 -m py_compile` on modified files, and run the applicable verification (`check`/`verify-quick`/`verify-extended`).

## Notes

- Never leave a verification run half-finished (it overwrites `experiments/*.json` then restores). If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Drivers run offline via `QUANT_RESEARCH_OFFLINE=1`; missing cached inputs fail hard.
- Lint: `python3 -m py_compile` on changed Python files. No separate linter configured.
- Do not commit or modify golden artifacts without explicit user request.

(End of file)
