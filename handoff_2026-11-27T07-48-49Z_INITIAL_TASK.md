# Durable Handoff — Next Agentic Work Session

**Created:** 2026-11-27T08:43:28Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Status:** No active task. Ready for the next session's first task.

## Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key conventions (read before acting)

- `experiments/*.json` are canonical research artifacts. Verification suite overwrites them while re-running drivers and restores them afterwards — **never leave a verification run half-finished**.
- Always run with `SEED=42`. Offline mode: `QUANT_RESEARCH_OFFLINE=1`.
- Baseline integrity: `scripts/check_goldens_clean.py` fails if a tracked artifact under `experiments/` differs from HEAD or a stale snapshot is pending. Recovery: `python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- Re-pinning an artifact requires `python3 scripts/check_golden_baseline.py --update` and a ledger entry.
- Cache coverage invariant: `scripts/check_data_coverage.py` resolves every `data.download()` call site; unpinned inputs fail under offline mode. To add an input, commit the file and re-pin.
- No separate linter; run `python3 -m py_compile` on changed files.
- Do NOT commit verification output. Do NOT commit unless explicitly asked.

## Verification commands

```bash
# Convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Individual drivers
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Pending work

None recorded. The next session should pick up a new task from the user and record it here.

## Notes for next agent

- This file is the durable handoff. Update it when starting/finishing work so context survives across sessions.
- Board posts and peer context may exist — check `board_read` before integrating with others' work.
