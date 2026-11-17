# Session Handoff

**Timestamp:** 2026-11-17T13:53:58Z

## Initial Task

Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.

## Project Context

This is a quantitative trading research repository (US equities, futures, macro data; 2014–2026). All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Files

- `AGENTS.md` — project commands, conventions, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — surviving strategies and experiment outcomes
- `experiments/*.json` — canonical research artifacts (golden files)
- `scripts/check.sh` — fast convention-robustness check + template validation
- `run_all_verification.py` — full verification suite

## Reproducibility Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
```

## Important Notes

- Never commit verification output; restore goldens before committing (`run_all_verification.py --restore-only`).
- Use `SEED=42` for all runs.
- `experiments/*.json` are canonical; verification suite backs them up before re-running.