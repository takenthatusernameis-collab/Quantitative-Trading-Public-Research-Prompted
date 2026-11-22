# Agentic Work Session Handoff

**Created:** 2026-11-22T20:53:00Z
**Status:** Initial task message — pending next session

## Task

No specific task defined yet. This is a durable handoff file for the next agentic work session. Leave your initial task message here before beginning work.

## Project Context

- Repository: Quantitative-Trading-Public-Research-Prompted
- Root: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- Research phase complete (E001–E043); surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical research artifacts: `experiments/*.json` (committed goldens, never modified by verification runs).
- Verification suite: `run_all_verification.py` backs up and restores `experiments/` goldens.

## Quick Start Commands

- Convention-robustness check (~seconds): `SEED=42 bash scripts/check.sh` or `make check`
- Full verify (~15 min): `SEED=42 python3 run_all_verification.py --full`
- Individual driver: `SEED=42 python3 experiments/run_e042.py --n-sim 50`

## Rules

- Always run `SEED=42` for reproducibility.
- Never commit verification output; restore goldens with `--restore-only` if a run is interrupted.
- Do not re-pin goldens to silence drift; see ledger open items.
- Data inputs must be pinned (cache coverage invariant) before offline runs.

## Notes for Next Session

- Check `git status` and `git log --oneline -10` before starting.
- Confirm no live verification run owns `.verify_snapshot/ACTIVE.json`.
