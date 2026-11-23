# Agentic Work Handoff

**Timestamp (UTC):** 2026-11-23T08:31:45Z
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial task for next session

No specific task was defined in this session. This file exists as the durable handoff anchor so the next agentic work session can record its own task here.

## Conventions to remember

- Always use `SEED=42`.
- `experiments/*.json` are committed golden artifacts; verification drivers overwrite them and restore them afterwards — never commit verification output.
- Reproducibility: run with `QUANT_RESEARCH_OFFLINE=1`; all data inputs must be pinned (tracked + SHA-256 in `ledger/data_baseline.json`).
- Lint/typecheck: run `python3 -m py_compile` on changed Python files (no separate linter configured).
- Commit messages should match repo style; only commit when explicitly asked.
- `src/portfolio_opt.py` validates solver answers on the problem's constraints, never on solver exit status.
- `make check` = `SEED=42 bash scripts/check.sh` (~seconds, offline).

## Board

Use `board_post`/`board_read` for peer coordination when multiple agents are involved. This session's row is flagged self: true; do not post to yourself.