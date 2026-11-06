# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-06T23-38-28Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 8b4d056
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Working tree clean; no active verification run; `.verify_snapshot/` absent. Golden artifacts under `experiments/` match HEAD.
- No research actions taken in this session beyond this handoff.

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !*
- Created this durable handoff file following the established pattern (root copy + `handoff/` copy + root symlinks).

## Initial Task

**CLEAR INITIAL TASK:** Do not invent a research task or run verification unprompted. Inspect the actual repository state (`git status`, `scripts/check.sh`), verify goldens/data baselines are intact, then per `PROMPT.MD` select and execute the highest-value next research task (discover/reproduce/validate a quantitative strategy), recording evidence and ending the session with a new durable handoff.

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents; use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Durable copies written to: root, `handoff/`. Root symlinks `INITIAL_TASK.md`, `NEXT_HANDOFF.md`, `LATEST.md`, `handoff.md`, `next_session.md`, `next_session_handoff.md` updated to point here.
Handoff written by agent at 2026-11-06T23-38-28Z.
