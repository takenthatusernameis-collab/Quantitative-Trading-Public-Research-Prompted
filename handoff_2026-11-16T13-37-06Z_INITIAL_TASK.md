# Handoff — agentic work session

**Created:** 2026-11-16T13:37:37Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Outstanding task

None assigned yet. No specific software engineering task was given in this session.

## Next steps for the next session

1. Ask the user for the task, or pick up the highest-priority open item from `ledger/RESEARCH_LEDGER.md`.
2. Read `AGENTS.md` before running any commands (seed `SEED=42`, offline mode `QUANT_RESEARCH_OFFLINE=1`, golden artifacts under `experiments/` must not be committed).
3. Verify changes with `SEED=42 bash scripts/check.sh` and `python3 -m py_compile` on changed files.
4. Do not commit unless explicitly asked.

## Relevant conventions

- `experiments/*.json` are canonical research artifacts — never modify directly; verification backs them up and restores them.
- `data/` cache files are gitignored except pinned vintages; check `ledger/data_baseline.json` before adding inputs.
- Tangency/QP determinism: validate solver answers on constraints, not exit status (`src/portfolio_opt.py`, `tests/test_portfolio_opt.py`).
