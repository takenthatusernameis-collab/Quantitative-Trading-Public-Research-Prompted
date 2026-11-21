# Handoff — Quantitative-Trading Research

**Created:** 2026-11-21T20:06:44Z
**Branch:** default (git repo)
**Status:** idle — no pending task

## Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key conventions (from AGENTS.md)

- Never leave `experiments/*.json` half-finished after a verification run — they are backed up/restored by `run_all_verification.py`.
- Always run with `SEED=42`.
- Never commit verification output; restore via `--restore-only` if interrupted.
- Data inputs must be pinned (`ledger/data_baseline.json`, `ledger/golden_baseline.json`) — offline mode `QUANT_RESEARCH_OFFLINE=1`.
- `cvxpy`/`cvxopt` optional; optimizer falls back to scipy.

## Common commands

```bash
SEED=42 bash scripts/check.sh          # convention robustness + template validation (~seconds)
SEED=42 python3 run_all_verification.py --skip-slow   # convention only, skip slow batch
SEED=42 python3 run_all_verification.py               # quick full (~8 min)
SEED=42 python3 run_all_verification.py --extended    # extended (~21 min)
SEED=42 python3 run_all_verification.py --full        # full (~15 min)
python3 -m py_compile <file>            # lint/typecheck equivalent
```

## Where to start

No task currently assigned. Check `ledger/RESEARCH_LEDGER.md` for standing dispositions and open items (e.g., E041/E042 optimizer determinism ill-conditioned QP drift). When a task arrives, search the codebase first, implement, verify with the commands above, and do not commit unless explicitly asked.
