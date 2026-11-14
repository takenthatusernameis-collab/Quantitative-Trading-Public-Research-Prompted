# Durable Handoff — Initial Task Message

## Timestamp
Created: 2026-11-14T00:55:03Z

## Repo
`/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Purpose
Leave a clear initial task for the next agentic work session.

## Open Task
None yet — this is the initial handoff placeholder. The next agentic session should first inspect the board (`board_read`) for peer context and any pending updates before starting new work.

## Convention Reminders
- Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are canonical research artifacts — never commit verification output.
- Reproducibility: always use `SEED=42`; `QUANT_RESEARCH_OFFLINE=1` for verification.
- Golden integrity: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard artifacts.
- Data coverage invariant: `scripts/check_data_coverage.py` — every `data.download()` call site must have a tracked, pinned cache file.
- No separate linter; run `python3 -m py_compile` on changed files.
- Never commit unless explicitly asked.
