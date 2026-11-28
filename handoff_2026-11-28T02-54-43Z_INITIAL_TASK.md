# Durable Handoff — Quantitative Trading Research

**Created:** 2026-11-28T03:54:52Z
**Session:** ses_ddfb5969cffeth04vQBPS0Qlm5
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Clear initial task for next agentic session

Run the fast convention-robustness check (offline, seconds) and report results:

```bash
SEED=42 bash scripts/check.sh
# or equivalently: make check
```

This validates JSON experiment artifacts, golden baselines, data coverage, and runs the portfolio_opt determinism test. It does not touch the network and does not overwrite committed goldens.

## Context

- Research phase complete (E001–E043); validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are canonical research artifacts — never commit verification output.
- If `check.sh` reports a golden mismatch, fix before committing.
- Lint: `python3 -m py_compile` on changed files (no separate linter configured).
- Full verification: `SEED=42 python3 run_all_verification.py --verify-quick` (~8 min).

## Board state

Board is empty; no pending peer coordination. No HOLD/VETO in effect.
