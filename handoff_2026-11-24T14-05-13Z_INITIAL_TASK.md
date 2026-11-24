# Durable Handoff — Quantitative-Trading-Public-Research-Prompted

**Created:** 2026-11-24T14:09:49Z
**Next agentic work session:** initial task message below.

## Initial task

No specific task was assigned yet for the next session. When you resume:

1. Check `git status` and `git diff` to confirm the working tree is clean and no golden artifacts under `experiments/` were left replaced by a verification run.
2. If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
3. Run the convention-robustness check: `SEED=42 bash scripts/check.sh` (or `make check`).
4. Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` before making any changes — research phase is complete (E001–E043); `experiments/*.json` are committed goldens that must never be modified by verification output.
5. Pick up whatever task the user provides next; there is no open bug, feature, or investigation currently in flight.

## Key conventions (from AGENTS.md)

- Seed: always `SEED=42`.
- `experiments/*.json` are canonical research artifacts / goldens. Verification backs them up and restores them; a half-finished run leaves driver output in the working tree — restore before committing.
- Lint/typecheck: `python3 -m py_compile` on changed files (no separate linter configured).
- Dependencies: `pip install -r requirements.txt`.
- Offline drivers run with `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard.
