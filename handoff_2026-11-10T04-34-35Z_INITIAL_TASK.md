# HANDOFF — Initial Task (next agentic work session)

**Created:** 2026-11-10T04:34:35Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Status:** No specific task assigned yet. Awaiting user instruction for the next work item.

## Context
- Quantitative-strategy research repo (2014–2026 US equities, futures, macro). Research phase complete (E001–E043); validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Python 3. Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional.
- Committed golden artifacts: `experiments/*.json` (never commit verification output).
- Verification commands: `SEED=42 bash scripts/check.sh` (fast), `SEED=42 python3 run_all_verification.py --verify-quick` / `--verify-extended` / `--verify-full`.
- Offline mode: `QUANT_RESEARCH_OFFLINE=1`; data inputs must be pinned in `ledger/data_baseline.json` (`scripts/check_data_coverage.py --update` to add).
- `src/portfolio_opt.py` validates solver answers on constraints, never exit status (ledger E049). Tangency QP is ill-conditioned (~1e-05 drift); do not re-pin E041/E042 goldens to silence drift.

## Next session initial task
None defined. On session start:
1. Read this file (`handoff_CURRENT.md` / `handoff_LATEST.md`).
2. Ask the user for the specific task, or check the shared board for pending work.
3. If no task: run `SEED=42 bash scripts/check.sh` to confirm baseline integrity, then idle awaiting instruction.

## Durable links
`handoff_CURRENT.md`, `handoff_LATEST.md`, `handoff_NEXT_SESSION.md`, `handoff_INITIAL_TASK.md` all symlink to this file.
