# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-02T08:38:48Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**State:** Research phase complete (E001–E057). Baseline verified clean. No open research task.

## Initial task message for the next agentic work session

> **START HERE:** The repository is genuinely done. There is no open task. Wait for the user to give you a new instruction; do not invent one. Do **not** re-run `scripts/check.sh` to "confirm" the baseline. Do **not** write another handoff unless the user asks.

**If the user gives no new instruction, your entire job is to report status and stop.**

## Constraints (standing, non-negotiable)

- Never commit verification output; restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only`).
- Never re-pin goldens to silence drift.
- Preserve pre-registrations; do not change gate logic, falsification expectations, or sensitivity grids.
- Honor pinned caches (`data/vintages.json`, `data/fundamentals/`, `ledger/data_baseline.json`); suite runs with `QUANT_RESEARCH_OFFLINE=1`.
- Always use `SEED=42`; run `python3 -m py_compile` on any script touched.
- CI is maintainer-gated: do not create/commit under `.github/workflows/`; use `.github/workflow-templates/verification-gate.yml`.
- Follow repo conventions in `AGENTS.md`.

## Quick references

- Checks: `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only`
- Docs: `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `README.md`

(End of file)
