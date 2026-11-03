# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-03T00:22:25Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main

## Clear initial task message for the next agentic session

> **START HERE:** The baseline is verified clean and the repository is closed. There is currently no open task in the queue. **Await explicit user instructions before taking any action.** Do **not** invent new tasks, re-run verification "just to be sure", create unprompted handoffs, or re-open closed items (E049/E050 optimizer determinism, E041/E042 QP drift). If the user provides a specific task, confirm scope against `AGENTS.md` before making changes.

## Standing constraints (must follow)

- Never commit verification output; restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only`).
- Never re-pin goldens to silence drift; only via `python3 scripts/check_golden_baseline.py --update` with explicit ledger justification.
- Honor pinned cache vintages (`data/vintages.json`, `data/fundamentals/` per `data/fundamentals_vintages.json`, `ledger/data_baseline.json`); verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without explicit justification and a ledger entry.
- Follow repo conventions in `AGENTS.md` (SEED=42, `python3 -m py_compile` on touched scripts).
- Do not create/modify GitHub workflows (`.github/workflows/`); use `make check` / `make verify` locally.

## References

- `ledger/RESEARCH_LEDGER.md` (last entry E068; E001–E043 research experiments complete)
- `AGENTS.md`
- Previous handoff: `HANDOFF_NEXT_SESSION_LATEST.md` (superseded by this file)
- This handoff: `HANDOFF_NEXT_SESSION_2026-11-03T00-22-25Z.md`
