# Handoff — Next Agentic Work Session

**Created:** 2026-11-21T18:03:24Z
**Root:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial task
No specific task was left for the next session. The working tree is idle.

## Common entry points
- Convention check (fast, offline): `SEED=42 bash scripts/check.sh` (or `make check`)
- Quick full verification (~8 min): `SEED=42 python3 run_all_verification.py` (or `make verify-quick`)
- Typecheck / compile changed Python: `python3 -m py_compile <file>`

## Repo notes (from AGENTS.md)
- `experiments/*.json` are canonical research artifacts — never commit verification output over them.
- Offline runs: `QUANT_RESEARCH_OFFLINE=1`.
- Seed: always `SEED=42`.
