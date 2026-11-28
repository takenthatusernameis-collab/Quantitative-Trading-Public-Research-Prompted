# Agentic Handoff — Quantitative-Trading-Public-Research-Prompted

**Created:** 2026-11-28T06:31:59Z
**Session:** New session — 2026-11-28T06:31:59Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial task message for the next agentic work session

> No pending engineering task. Research phase is complete (E001–E043); surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
>
> Baseline verification status is clean as of this handoff. Before any change, run:
>
> ```bash
> SEED=42 bash scripts/check.sh
> ```
>
> If you are asked to make a change, pre-register it per the project conventions, record it in `ledger/RESEARCH_LEDGER.md`, and never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect of verification.

## Key context

- `experiments/*.json` are committed golden artifacts; a verification run must never be left half-finished.
- Re-pinning goldens is only warranted if a deliberate code change alters a published number, recorded in the ledger first (see E050 precedent).
- No separate linter configured; run `python3 -m py_compile` on changed files.

## Never do

- Do not commit verification output / driver output into `experiments/`.
- Do not re-pin goldens as a side effect of verification.
