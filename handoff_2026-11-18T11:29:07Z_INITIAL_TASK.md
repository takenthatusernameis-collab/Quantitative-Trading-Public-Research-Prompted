# Handoff Message

**Timestamp:** 2026-11-18T11:30:20Z

## Initial Task

Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.

## Workspace Context

- **Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Project:** Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase:** Complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Key conventions:** `SEED=42`, close-to-close primary convention, cached parquet data in `data/`, golden artifacts in `experiments/*.json`.

## Relevant Commands

```bash
SEED=42 bash scripts/check.sh          # Fast convention-robustness check
SEED=42 python3 run_all_verification.py --full  # Full verification
SEED=42 python3 run_all_verification.py --restore-only  # Recover golden artifacts
```

## Notes

- This handoff file is the durable initial task message for the next agentic work session.
- The baseline integrity rules in `AGENTS.md` must be respected: verification runs back up and restore `experiments/*.json`; never commit verification output without restoring goldens first.