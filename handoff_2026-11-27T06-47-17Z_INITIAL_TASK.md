# Initial Task — Handoff for Next Agentic Work Session

**Created:** 2026-11-27T06:47:17Z
**Session:** handoff_2026-11-27T06-47-17Z
**Repo:** Quantitative-Trading-Public-Research-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Purpose

Durable handoff message for the next agentic work session. Leave this message in place so the next session knows the current task context without re-discovery.

## Current Task

> Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.

**Status:** COMPLETE (this file).

## Repo Conventions (read before acting)

- `experiments/*.json` are canonical research artifacts — the verification suite overwrites them while re-running drivers and restores them afterwards. Never leave a verification run half-finished.
- Baseline integrity: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` are first-class steps in `scripts/check.sh`. Do not re-pin artifacts as a side effect of verification.
- Use `SEED=42` for all runs. `QUANT_RESEARCH_OFFLINE=1` during verification so missing cache entries fail hard.
- Commands: `make check` / `make verify` / `make verify-quick` / `make verify-extended` / `make verify-full`.
- `python3 -m py_compile` on changed Python files (no separate linter configured).
- Do NOT commit verification output. Do NOT commit unless explicitly asked.

## Verification Drivers (quick block: 5a)

E012, E023, E024 (--merge), E027, E035, E037, E039, E042-lead.

Extended block adds: E011, E013, E015–E022, E025, E026, E028–E030, E034, E036, E041.

## Data Coverage

Every `data.download()` call site in drivers must have a git-tracked cache file matching the SHA-256 pinned in `ledger/data_baseline.json`. Unpinned inputs are live network downloads (yfinance is not bit-reproducible). To add an input, commit the file and re-pin: `python3 scripts/check_data_coverage.py --update`.

## Notes

- No commits were made in this session.
- No code changes were made in this session.
- No pending blockers.
