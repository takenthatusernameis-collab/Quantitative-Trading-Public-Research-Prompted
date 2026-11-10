# HANDOFF — Initial Task (next agentic work session)

**Created:** 2026-11-10T04:37:01Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Status:** No specific task assigned. Awaiting user instruction.

## Project context (read first)
- Research phase complete (E001–E043). Validated strategies and standing issues: `ledger/RESEARCH_LEDGER.md`.
- Canonical golden artifacts: `experiments/*.json` pinned in `ledger/golden_baseline.json`; data/cache coverage pinned in `ledger/data_baseline.json` / `data/vintages.json`.
- Reproducibility: always `SEED=42`. Verification runs overwrite then restore goldens; if interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`. Never commit verification output or re-pin goldens as a side effect of verification.
- Known open item: E041/E042 optimizer/tangency-QP ill-conditioning can drift (~1e-05, 1-ulp sensitivity); do not re-pin to silence drift (ledger E049).
- Working tree note at handoff time: modified `__pycache__/*.pyc` under `scripts/`, `src/`, `tests/` (12 files) — avoid committing them.

## Baseline check
```bash
SEED=42 bash scripts/check.sh                 # fast integrity/convention check
# optional: make verify-quick                 # ~8 min
# recovery: SEED=42 python3 run_all_verification.py --restore-only
```

## Initial task for next session
1. Read this handoff (also via `handoff_CURRENT.md` / `handoff_LATEST.md` / `handoff_NEXT_SESSION.md`).
2. Check for pending coordination: `board_read` (if peer context relevant) and ask the user for the specific task/priority.
3. If no task is provided: run `SEED=42 bash scripts/check.sh`, report integrity status and any drift/issues, then await explicit instruction. Do not start new experiments, modify/re-pin goldens or baselines, or create commits without an explicit request.

## Durable pointers
Update/use convenience symlinks to this file for discoverability: `handoff_CURRENT.md`, `handoff_LATEST.md`, `handoff_NEXT_SESSION.md`, `handoff_INITIAL_TASK.md`, `handoff_next.md`.
