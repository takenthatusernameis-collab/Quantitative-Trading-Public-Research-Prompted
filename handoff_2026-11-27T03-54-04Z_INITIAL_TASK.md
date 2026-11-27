# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp**: 2026-11-27T03:54:04Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Durable artifact**: `handoff_2026-11-27T03-54-04Z_INITIAL_TASK.md` (repo root)

## Initial Task (for the next agentic work session)

Research phase is closed (E001–E043). Real work only, then stop.

1. Provision environment: `pip install -r requirements.txt` (numpy/pandas missing).
2. Reproduce: `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift. Do NOT re-pin artifacts.
3. Confirm E041/E042 reproduce with 0 differences under E050 exact active-set solver.
4. Cleanup (propose only): 9,135/9,678 tracked files are handoff artifacts; propose .gitignore + git rm --cached plan, let user decide.
5. Leave one handoff, then stop. Do not manufacture refreshes.

## Baseline Integrity (2026-11-27T03:54:04Z)

- No active verification run; goldens match HEAD; all 107 pinned goldens match baseline; all 35 pinned data inputs present/tracked/unchanged.
- Missing dependency: numpy/pandas not importable.

## Git State

- Branch main; HEAD `4cc711ef` == origin/main. No tracked source changes.

## Quick Start

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --restore-only
```