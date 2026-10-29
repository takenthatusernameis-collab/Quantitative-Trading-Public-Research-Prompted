# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-29T03:04:39Z
**Session status:** clean working tree (no uncommitted changes). Ready for new work.
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project context
Independent reproducible quantitative-strategy research (2014–2026 US equities, futures, macro). Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`. Committed artifacts live in `experiments/*.json` (canonical baselines, pinned in `ledger/golden_baseline.json`).

## Clear initial task message for next session
**TASK:** Awaiting user instruction.

### Immediate first steps (required)
1. Read `AGENTS.md` to understand conventions and baseline integrity rules.
2. Establish a clean baseline before making changes:
```bash
SEED=42 bash scripts/check.sh
```
   - If green, proceed only when the user provides a concrete objective.
   - If goldens are dirty from a prior interrupted run, restore first: `SEED=42 python3 run_all_verification.py --restore-only`.

### When working on a task
- Read relevant drivers/tests in `experiments/`, `src/`, and `tests/` before changing code.
- Make minimal, targeted changes following existing patterns.
- Run `python3 -m py_compile` on all modified Python files.
- Run the appropriate verification:
  - Quick checks: `SEED=42 bash scripts/check.sh` or `make check`
  - Feature/experiment changes: `SEED=42 python3 run_all_verification.py` (verify-quick) as appropriate
  - Broader changes: `SEED=42 python3 run_all_verification.py --extended` / `--full` only if necessary
- **Never commit or modify golden artifacts** without explicit user request.
- **Never leave a verification run half-finished** - it overwrites and restores `experiments/*.json`. If interrupted, always restore.
- Drivers run offline via `QUANT_RESEARCH_OFFLINE=1`; missing cached inputs fail hard.
- `cvxpy`/`cvxopt` optional; portfolio optimizer falls back to `scipy.optimize`.

## Baseline integrity (critical)
- `experiments/*.json` are overwritten by verification runs and restored afterwards — never leave a run half-finished; never commit verification output.
- `scripts/check_goldens_clean.py` fails if a tracked artifact under `experiments/` differs from HEAD or a stale snapshot is pending.
- `scripts/check_golden_baseline.py` compares every `experiments/` artifact to the SHA-256 pinned in `ledger/golden_baseline.json`. Replacing an artifact requires `--update`.
- `scripts/check_data_coverage.py` requires every `data.download()` cache file to exist, be git-tracked, and match `ledger/data_baseline.json` (runs offline with `QUANT_RESEARCH_OFFLINE=1`).

## Key commands (from AGENTS.md)
- `SEED=42 bash scripts/check.sh` — fast convention-robustness + template validation (~seconds, offline)
- `SEED=42 python3 run_all_verification.py` — verify-quick (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — verify-extended (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — verify-full (~15 min)
- `SEED=42 python3 run_all_verification.py --restore-only` — recover goldens after interrupted run
- `python3 -m py_compile` on changed files (no separate linter)

(End of file)
