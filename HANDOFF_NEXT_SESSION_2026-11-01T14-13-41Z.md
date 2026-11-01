# Durable Handoff — Initial Task Message

**Timestamp:** 2026-11-01T15:03:20Z
**Created by:** Kilo (agentic session)

## Task for next session

Leave a timestamped, clear initial task message for the next agentic work session in a durable handoff.

## Context

- Working directory: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- This is an independent reproducible quantitative-strategy research repository (US equities, futures, macro 2014–2026).
- Research phase complete (E001–E043); surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical research artifacts live in `experiments/*.json` — verification suite backs them up and restores them; never leave a verification run half-finished.
- Key commands (see `AGENTS.md`):
  - `SEED=42 bash scripts/check.sh` — convention-robustness check + template validation
  - `SEED=42 python3 run_all_verification.py --skip-slow` — quick verification
  - `python3 -m py_compile <file>` — compile check on changed Python files
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).

## Next actions

1. Read this `HANDOFF.md` and `AGENTS.md`.
2. Resume / continue the outstanding quantitative research task.
3. Run `SEED=42 bash scripts/check.sh` before committing any changes.
4. Do not commit unless explicitly asked; restore goldens after any verification run (`--restore-only`).
