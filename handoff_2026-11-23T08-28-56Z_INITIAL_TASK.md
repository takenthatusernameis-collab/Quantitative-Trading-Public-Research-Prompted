# Agentic Work Handoff

**Timestamp (UTC):** 2026-11-23T08:28:56Z
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial task for next session

No specific task was defined in this session. This file exists as the durable handoff anchor so the next agentic work session can record its own task here.

## Project State Summary

**Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

- **Completed experiments:** 43 (E001–E043)
- **Validated strategies:** Long-term reversal, low-vol anomaly, 6-month momentum, value (all with strong OOS z-scores vs placebo)
- **Rejected/Partial:** Cointegration stat-arb (E025), market-neutral portfolio (E041), min-var confirmatory (E042 - PARTIAL)
- **Verification suite:** 8 drivers in quick verify, 26 total committed drivers in extended

## Conventions to remember

- Always use `SEED=42`.
- `experiments/*.json` are committed golden artifacts; verification drivers overwrite them and restore them afterwards — never commit verification output.
- Reproducibility: run with `QUANT_RESEARCH_OFFLINE=1`; all data inputs must be pinned (tracked + SHA-256 in `ledger/data_baseline.json`).
- Lint/typecheck: run `python3 -m py_compile` on changed Python files (no separate linter configured).
- Commit messages should match repo style; only commit when explicitly asked.
- `src/portfolio_opt.py` validates solver answers on the problem's constraints, never on solver exit status.
- `make check` = `SEED=42 bash scripts/check.sh` (~seconds, offline).

## Quick Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; quick + 18 more committed drivers)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
```

## Board

Use `board_post`/`board_read` for peer coordination when multiple agents are involved. This session's row is flagged self: true; do not post to yourself.