# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-06T22-58-18Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- No active verification run; `.verify_snapshot/` absent. Golden artifacts under `experiments/` match HEAD.
- No source/test/ledger changes in this session. Only handoff file added.

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*
- Created this durable handoff file. No research actions taken.

## Initial Task

**CLEAR INITIAL TASK:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, change baselines, or invent tasks unprompted.

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents; use local `make check/verify/*`.

## Handoff provenance

Durable copies written to: `handoff/`, `.kilo/handoff/`. Root symlinks updated as applicable.
Handoff written by agent at 2026-11-06T22-58-18Z.
