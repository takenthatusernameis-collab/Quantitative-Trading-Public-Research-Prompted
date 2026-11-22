# Durable Handoff — Initial Task

**Created:** 2026-11-22T23:38:36Z
**Session:** previous agentic work session
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Task

Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.

## Status

Complete — this handoff file was written by the previous session at the timestamp above.

## Next steps for the next session

- No further work is required on this task.
- Review `AGENTS.md` for project commands and conventions before continuing any research work:
  - `SEED=42 bash scripts/check.sh` — fast convention-robustness check (~seconds, offline)
  - `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min)
  - `make check` / `make verify` / `make verify-extended` / `make verify-full`
- Never commit verification output; if a verification run is interrupted, restore goldens first via `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- `experiments/*.json` are canonical research artifacts; do not modify them except through the verification suite which restores them afterward.
- No separate linter configured; run `python3 -m py_compile` on changed Python files.
- Seed is always `SEED=42` (walk-forward + placebo RNG).
