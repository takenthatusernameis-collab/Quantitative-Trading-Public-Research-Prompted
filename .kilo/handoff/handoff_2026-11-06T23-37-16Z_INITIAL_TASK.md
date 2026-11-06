# Initial Task Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-06T23:37:16Z
**Created by:** Glyph Cluster session (handoff request)
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch:** `main`
**HEAD:** `576b99f` (`chore: capture completed workflow run diagnostics`)
**Working tree at handoff creation:** no uncommitted changes to `experiments/`, `data/`, `ledger/golden_baseline.json`, or `ledger/data_baseline.json`. `.verify_snapshot/` not present. New handoff files created by this session are expected working-tree additions.

## Clear initial task for the next session

**Wait for explicit user instructions before taking any action.**

Do **not**:
- run verification, batch runs, or experiment drivers “just to be sure”;
- modify, regenerate, or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, or `ledger/data_baseline.json`;
- change `data/` inputs, `data/vintages.json`, or `data/fundamentals_vintages.json`;
- invent new research tasks, re-open closed items (E001–E092 complete; E049/E050 and E041/E042 drift handling are closed per ledger/AGENTS.md), or move pre-registered goalposts;
- create commits/PRs or create/modify `.github/workflows/` unless explicitly requested.

If the user explicitly requests work, follow `AGENTS.md` exactly: `SEED=42`, close-to-close primary convention, pre-registration/multiple-testing discipline, honest negative results, and baseline-integrity guards.

## Quick state verification (only if needed)

```bash
git log -1 --oneline
git status --short
git diff --name-only HEAD -- experiments/ data/ ledger/golden_baseline.json ledger/data_baseline.json
ls -la .verify_snapshot 2>&1 | head
SEED=42 bash scripts/check.sh        # only if explicitly requested / needed
```

If a verification run is interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (never commit verification output).

## Key references

- `AGENTS.md` — commands, reproducibility, golden/data baseline rules
- `ledger/RESEARCH_LEDGER.md` — research history and dispositions
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `run_all_verification.py` (`--quick` / `--extended` / `--full` / `--skip-slow` / `--restore-only`)

## Provenance

- Durable handoff: `handoff/handoff_2026-11-06T23-37-16Z_INITIAL_TASK.md`
- Supersedes prior “latest” pointers by convention; prior handoffs remain in history.
