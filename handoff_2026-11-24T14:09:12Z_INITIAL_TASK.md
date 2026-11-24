# Initial Task — Next Agentic Work Session

Timestamp: 2026-11-24T14:09:12Z

## Status
Fresh session start. No in-progress work carried over. Repository is at research-complete state (E001–E043); canonical golden artifacts live under `experiments/`.

## First Actions for Incoming Agent
1. Read `AGENTS.md` for project commands, conventions, and verification gates.
2. Run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm baseline integrity before any edits.
3. If verification artifacts are dirty, restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
4. Check `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` pass before committing anything.

## Standing Rules
- Use `SEED=42` for all runs.
- Never commit verification output; restore goldens after interrupted runs.
- Re-pin artifacts only via documented scripts, never as a side effect of running the suite.
- Do not create CI workflow files (`.github/workflows/`); use the template in `.github/workflow-templates/`.

## Open Items
- None specified. Awaiting user instruction for next task.
