# Durable Handoff — Initial Task

**Session start:** 2026-11-22T20:52:45Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Pending task

Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.

## Status

This handoff message was created as the initial task record. No further work has been committed yet.

## Context / conventions

- Repo is a quantitative-strategy research project (Python 3). Baseline artifacts live in `experiments/*.json`.
- Never commit changes unless explicitly asked.
- Verification: `SEED=42 bash scripts/check.sh` or `make check`.
- Do not leave `experiments/` overwritten from a half-finished verification run; recover with `SEED=42 python3 run_all_verification.py --restore-only`.
- No separate linter; run `python3 -m py_compile` on changed files.
