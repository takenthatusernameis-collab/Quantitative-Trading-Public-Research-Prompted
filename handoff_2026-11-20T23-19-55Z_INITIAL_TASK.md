# Handoff — agentic work session

**Created:** 2026-11-20T23:20:55Z

## Pending task

Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.

## Status

Complete — this HANDOFF.md is the durable handoff marker. No code changes were required.

## Notes

- This is a quantitative-strategy research repo (2014–2026 US equities, futures, macro).
- Baseline artifacts: `experiments/*.json` are committed goldens; verification overwrites then restores them — never commit verification output.
- Relevant commands: `SEED=42 bash scripts/check.sh` (fast), `SEED=42 python3 run_all_verification.py --verify-quick`/`--extended`/`--full`.
- `AGENTS.md` documents baseline integrity, reproducibility, cache coverage, CI templates, and commit conventions (no empty commits, never amend failed commits).
- Do NOT commit unless explicitly asked.
