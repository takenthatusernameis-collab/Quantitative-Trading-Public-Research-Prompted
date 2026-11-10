# HANDOFF — Initial Task (next agentic work session)

**Created:** 2026-11-10T04:35:00Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Status:** No specific task assigned. Awaiting user instruction for the next work item.

## Context (read before acting)
- **Project:** Reproducible quantitative-strategy research on 2014–2026 US equities/futures/macro. Research phase complete (E001–E043); validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` are golden baselines pinned in `ledger/golden_baseline.json`. Do **not** commit verification output or re-pin goldens as a side effect of running verification. If interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per AGENTS.md).
- **Data:** Pinned vintages in `data/vintages.json` / `ledger/data_baseline.json`; E029 fundamentals pinned. Drivers run with `QUANT_RESEARCH_OFFLINE=1` in verification; adding inputs requires committing the cache and `python3 scripts/check_data_coverage.py --update`.
- **Reproducibility:** Always use `SEED=42`. `src/portfolio_opt.py` validates solver answers on constraints (not exit status, ledger E049); tangency QP is ill-conditioned (~1e-05 drift) — do not re-pin E041/E042 to silence drift.
- **Working tree note:** `git status` shows modified `__pycache__/*.pyc` under `scripts/`, `src/`, `tests/` (untracked build artifacts in effect); avoid committing them.

## Quick verification
```bash
SEED=42 bash scripts/check.sh          # fast integrity/convention check
make verify-quick                      # ~8 min (8 drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens if interrupted
```

## Next session initial task
1. Read this handoff (`handoff_CURRENT.md` / `handoff_LATEST.md` / `handoff_NEXT_SESSION.md`).
2. Ask the user for the specific task, or check the shared board (`board_read`) for pending work.
3. If no task is given: run `SEED=42 bash scripts/check.sh` to confirm baseline integrity, report the result, and await instruction. Do not start new experiments, modify goldens, or push commits without an explicit request.

## Durable links
`handoff_CURRENT.md`, `handoff_LATEST.md`, `handoff_NEXT_SESSION.md`, `handoff_INITIAL_TASK.md` (and related convenience symlinks) point to this file.
