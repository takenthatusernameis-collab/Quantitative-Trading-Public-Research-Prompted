# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-25T19:26:06Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch**: `main`
**Working tree**: clean
**Last commit**: `1643f062 chore(kilo): checkpoint agent session`

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Initial Task (next session)
Default: await explicit user instructions. If acting autonomously:
1. Verify working-tree cleanliness against HEAD (`git status`).
2. Run `SEED=42 bash scripts/check.sh` (fast convention-robustness check).
3. If clean, reproduce with `SEED=42 python3 run_all_verification.py --extended` and report any drift; do NOT re-pin goldens.
4. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` before committing anything.

## Quick Commands
```bash
SEED=42 bash scripts/check.sh            # fast check (~seconds, offline)
SEED=42 python3 run_all_verification.py  # quick verification (~8 min)
SEED=42 python3 run_all_verification.py --extended  # extended (~21 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover interrupted run
pip install -r requirements.txt          # provision dependencies if needed
```

## Key Notes
- Always use `SEED=42` for reproducibility.
- `experiments/*.json` are canonical golden artifacts — never commit verification output.
- `QUANT_RESEARCH_OFFLINE=1` is enforced during verification.
- `src/portfolio_opt.py` validates solver answers on constraints, not solver exit status (ledger E049/E050).

## Last Verification Status
Run `SEED=42 python3 run_all_verification.py --extended` to verify current state; it re-executes committed drivers and compares against goldens with `numeric_tol=1e-4`.
