# Agentic Handoff — Initial Task

**Session start:** 2026-11-17T23:31:05Z
**Workspace root:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Persistent branch:** none detected (working tree clean unless interrupted)

## Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043); surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session

No new task was specified. Run the convention-robustness check + template validation as a smoke test, then report status:

```bash
SEED=42 bash scripts/check.sh
#   or
make check
```

If anything fails, inspect the failures and restore any half-finished state via:

```bash
SEED=42 python3 run_all_verification.py --restore-only
```

Do NOT commit unless explicitly asked. Canonical artifacts live in `experiments/*.json`; verification backs them up and restores them automatically — never leave a run half-finished.

## Key files

- `AGENTS.md` — project commands, conventions, baseline integrity rules
- `scripts/check.sh` / `make check` — convention-robustness + template validation
- `run_all_verification.py` — full/extended/quick verification suites
- `experiments/*.json` — committed golden artifacts (canonical baseline)
- `ledger/RESEARCH_LEDGER.md` — surviving validated strategies
