# Agent Handoff — Kilo session

**Timestamp:** 2026-11-24T03:17:16Z

## Status
- Repository root: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- Branch: clean except `src/__pycache__/cache_keys.cpython-312.pyc` (modified, untracked pyc — not part of baseline)
- Last commit: `175bab9b chore(kilo): checkpoint agent session`

## Project context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Canonical research artifacts live in `experiments/*.json`.

## Next task (initial message for next session)
No specific task assigned yet. This is a clear initial handoff placeholder.

When the next session starts, begin by:
1. Reading `AGENTS.md` (project commands & conventions).
2. Running `SEED=42 bash scripts/check.sh` (fast convention-robustness check + template validation).
3. Confirming no verification run is half-finished (`.verify_snapshot/ACTIVE.json` marker must not own a live pid; otherwise run `SEED=42 python3 run_all_verification.py --restore-only`).
4. Committing any intended changes only when explicitly asked by the user.

## Key commands
- `SEED=42 python3 run_all_verification.py` — verify-quick (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — verify-extended (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — verify-full (~15 min)
- `SEED=42 python3 verify_convention_robustness.py` — convention robustness only
- `python3 -m py_compile <file>` — compile-check a changed Python file

## Constraints
- Never commit verification output; restore goldens before committing (`run_all_verification.py --restore-only` or `git checkout -- experiments/`).
- `experiments/*.json` are canonical artifacts; verification overwrites them then restores them — never leave a run half-finished.
- `QUANT_RESEARCH_OFFLINE=1` is used during verification; unpinned data inputs fail hard.
- Seed: always `SEED=42`.
- Do not add comments to code unless asked.
