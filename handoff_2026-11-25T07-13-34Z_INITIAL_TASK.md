# Agentic Handoff — Initial Task Message

## Timestamp
Created: 2026-11-25T07:18:37Z

## Next session's initial task
This session produced no code changes. The next agentic work session should:

1. Re-read `AGENTS.md` fully (baseline integrity, reproducibility, convention robustness).
2. Check `git status` and `git diff` to confirm the working tree is clean (no captured verification output under `experiments/`).
3. If a verification run was interrupted, recover with:
   `SEED=42 python3 run_all_verification.py --restore-only`
   (or `git checkout -- experiments/`).
4. Then proceed with the next assigned research/engineering task.

## Project context
- Quantitative strategy research on 2014–2026 US equities, futures, macro. Research phase complete (E001–E043).
- Canonical artifacts: `experiments/*.json` (committed goldens). Verification overwrites then restores them — never leave a run half-finished.
- Offline mode: `QUANT_RESEARCH_OFFLINE=1`; cache coverage enforced via `scripts/check_data_coverage.py` + `ledger/data_baseline.json`.
- Seed: always `SEED=42`.
- Commands: `make check` / `make verify-quick` / `make verify-extended` / `make verify-full`.
- No separate linter; `python3 -m py_compile` on changed files.
- Never commit unless explicitly asked.
