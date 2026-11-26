# Agent Handoff — Quantitative-Trading-Public-Research-Prompted

**Created:** 2026-11-26T05:05:15Z
**Status:** Working tree clean at HEAD `15495fd6 chore(kilo): checkpoint agent session`
**Branch:** (check with `git branch --show-current`)

## Repo overview

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043); validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

Canonical artifacts: `experiments/*.json` (golden files, committed). Verification overwrites then restores them — **never leave a verification run half-finished**.

## Key conventions (read AGENTS.md fully before acting)

- Always run with `SEED=42`
- Reproducibility gates: `scripts/check.sh` (`make check`), `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- `experiments/*.json` must match SHA-256 pinned in `ledger/golden_baseline.json`; re-pin only via `python3 scripts/check_golden_baseline.py --update` and record in the ledger
- Data coverage invariant: every `data.download()` call site must have a git-tracked cache matching `ledger/data_baseline.json`; add inputs by committing the file then `python3 scripts/check_data_coverage.py --update`
- `src/portfolio_opt.py` validates solver answers on the problem's constraints, never on solver exit status (ledger E049/E050)
- Close-to-close is v1.2.3 primary convention; overnight decomposition reported alongside

## Commands

```bash
SEED=42 bash scripts/check.sh          # convention robustness + template validation (~seconds)
SEED=42 python3 run_all_verification.py   # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only   # recover goldens after interrupted run
python3 -m py_compile <changed files>   # lint equivalent
```

No separate linter configured. Do **not** commit verification output. Do **not** create `.github/workflows/` (controller restores it; token lacks push permission) — template at `.github/workflow-templates/verification-gate.yml`.

## No current task assigned

There is no active task waiting for the next session. When a new task arrives, start by reading `AGENTS.md`, then explore the relevant code under `src/` and `experiments/` before making changes.
