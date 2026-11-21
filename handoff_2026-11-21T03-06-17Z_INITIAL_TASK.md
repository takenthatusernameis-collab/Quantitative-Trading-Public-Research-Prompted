# Agentic Work Handoff — Initial Task

**Generated:** 2026-11-21T03:08:05Z
**Session:** handoff-initial
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Task

No specific task assigned yet. This is a clear initial handoff marker for the next agentic work session.

## Convention reminder (AGENTS.md)

- Never commit unless explicitly asked.
- Run `python3 -m py_compile` on changed Python files (no separate linter configured).
- `experiments/*.json` are canonical research artifacts — verification runs overwrite then restore them; never leave a run half-finished.
- Seed: always `SEED=42`. Offline env: `QUANT_RESEARCH_OFFLINE=1`.
- Data cache coverage is enforced: pinned inputs must exist in `data/`, be git-tracked, and match SHA-256 in `ledger/data_baseline.json`.

## Quick commands

```bash
SEED=42 bash scripts/check.sh          # convention robustness (~seconds)
SEED=42 python3 run_all_verification.py --verify-quick  # ~8 min
```

## Next step

Define the next concrete task, then proceed. If none is given, run `SEED=42 bash scripts/check.sh` to confirm the repo is in a clean state before starting new work.
