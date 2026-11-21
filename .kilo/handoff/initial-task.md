# Durable Handoff — Initial Task Message

**Created:** 2026-11-21T05:02:26Z
**Session:** New session — 2026-11-21T05:02:23.947Z
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Summary

Fresh session started. The shared board is empty (no prior messages). No `.kilo/` directory existed yet; this handoff file is the first durable artifact.

No code changes have been made in this session. The only action taken is writing this handoff message.

## Initial task for the next agentic work session

Review the repository state and confirm the verification suite runs cleanly:

1. `SEED=42 bash scripts/check.sh` — convention-robustness check + template validation (~seconds, offline).
2. `SEED=42 python3 run_all_verification.py --verify-quick` — re-execute the 8 drivers in the 5a block and compare to committed goldens.
3. If any golden differs, investigate before committing; do NOT re-pin as a side effect of a verification run.
4. Run `python3 -m py_compile` on any changed files.

## Relevant conventions (from AGENTS.md)

- `experiments/*.json` are committed golden artifacts; verification backs them up and restores them — never leave a run half-finished.
- A verification run must never be left half-finished; use `run_all_verification.py --restore-only` or `git checkout -- experiments/` to recover.
- Do not commit verification output.
