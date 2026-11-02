# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-02T02:44:00Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**State:** Research phase complete (E001–E050). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`. Baseline verified clean at HEAD. No live verification snapshot (`.verify_snapshot/` absent).

## Initial task message for the next agentic work session

> **START HERE:** The baseline is verified clean and the E049/E050 tangency-QP open item is **closed**. Confirm the clean baseline is still clean (`SEED=42 bash scripts/check.sh` + `git status --short`), then take up the next research task from the ledger — do **not** re-open the optimizer determinism item and do **not** re-pin goldens to silence drift.

1. `pip install -r requirements.txt` if the environment was reset.
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with `=== All checks passed ===`.
3. `git status --short` — confirm working tree clean. If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
4. Only after steps 1–3 pass cleanly, proceed to the next research task from `ledger/RESEARCH_LEDGER.md`.

## Constraints

- Never commit verification output; restore goldens first if interrupted.
- Never re-pin goldens to silence drift.
- Run `python3 -m py_compile` on changed files.
- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.

(End of file)
