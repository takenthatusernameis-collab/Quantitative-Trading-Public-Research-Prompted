# Agentic Work Session Handoff

**Created:** 2026-11-22T18:44:39Z
**Branch:** clean working tree (no uncommitted changes)
**Last commit:** dd099181 chore(kilo): checkpoint agent session
**Next task:** clear this initial placeholder — define and execute the next real work item

## Context

Quantitative trading research repository (2014–2026 US equities, futures, macro).
Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key conventions (read AGENTS.md before acting)

- `experiments/*.json` are canonical committed goldens — never modify as a side effect of verification.
- Reproducibility: always use `SEED=42`, `QUANT_RESEARCH_OFFLINE=1`.
- `scripts/check.sh` runs convention robustness + convention checks.
- `make check` / `make verify-quick` / `make verify-extended` / `make verify-full`.
- Do NOT commit unless explicitly asked.

## Verification quick-start

```bash
SEED=42 bash scripts/check.sh          # convention robustness + template validation
SEED=42 python3 run_all_verification.py --skip-slow   # skip slow batch/regression
```

## Open / next work

None defined yet. The next agentic session should determine the actual task from the user and write it here before starting.
