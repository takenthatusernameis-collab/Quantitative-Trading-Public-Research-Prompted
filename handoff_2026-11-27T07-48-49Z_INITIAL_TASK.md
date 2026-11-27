# Agentic Handoff — Initial Task Message

**Created:** 2026-11-27T08:47:18Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Status

No concrete coding task was assigned in this session. This is a durable placeholder handoff for the next agentic work session.

## Project context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043); surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. Canonical research artifacts: `experiments/*.json` (committed goldens).

## Key conventions (from AGENTS.md)

- Always run with `SEED=42`.
- `experiments/*.json` are committed goldens; verification backs them up and restores them — never leave a verification run half-finished, and never commit verification output.
- Recovery after an interrupted run: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- Replacing a golden requires re-pinning (`python3 scripts/check_golden_baseline.py --update`) and a ledger entry.
- Data inputs must be pinned (`scripts/check_data_coverage.py --update`); offline mode uses `QUANT_RESEARCH_OFFLINE=1`.
- Lint: `python3 -m py_compile` on changed files. No separate linter configured.

## Quick commands

```bash
SEED=42 bash scripts/check.sh          # convention check (~seconds, offline)
SEED=42 python3 run_all_verification.py --skip-slow   # convention + fast drivers
SEED=42 python3 run_all_verification.py --verify-quick  # 8 drivers (~8 min)
```

## Initial task for next session

None defined yet. The next agentic session should:
1. Clarify the actual task with the user (or treat this handoff as complete if no further work is needed).
2. If given a task, locate relevant code under `src/`, `experiments/`, `scripts/`, or `tests/` and follow repo conventions.
3. Verify with `make check` / `python3 -m py_compile` before considering the work done.
