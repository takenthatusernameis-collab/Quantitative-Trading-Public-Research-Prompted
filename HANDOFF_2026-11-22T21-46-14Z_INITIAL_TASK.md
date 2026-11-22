# Initial Task — Handoff

**Timestamp:** 2026-11-22T21:46:14Z
**Session:** next agentic work session
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Purpose

Leave a durable, timestamped clear initial task message so the next agentic session can resume without ambiguity.

## Project context

Quantitative-strategy research repo on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043); surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

Canonical artifacts: `experiments/*.json` (committed goldens). Verification re-runs drivers and restores them afterwards — never leave a verification run half-finished.

## Immediate next task

Run the convention-robustness / quick verification gate to confirm the working tree is clean and reproducible:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If anything fails, fix it before committing. Do not commit verification output.

## Key conventions

- Always use `SEED=42`.
- `python3 -m py_compile` on any changed Python file (no separate linter configured).
- `experiments/*.json` are canonical; never modify as a side effect of verification.
- Data cache coverage is enforced: add inputs via `scripts/check_data_coverage.py --update`.
- CI verification-gate workflow cannot be created by automated agents; see `.github/workflow-templates/verification-gate.yml` and `VERIFICATION_GATE_TEMPLATE.md`.

## Handoff notes

- This is an initial/clear task message: no open code changes are assumed in progress.
- Previous handoff files exist in this directory (e.g. `HANDOFF_CURRENT.md`, `HANDOFF_NEXT_SESSION_*.md`, `HANDOFF_SESSION_*.md`) for reference.
