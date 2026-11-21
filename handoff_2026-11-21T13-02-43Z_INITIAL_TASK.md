# Durable Handoff — Initial Task Message

## Timestamp
2026-11-21T13:04:10Z

## Context
Quantitative-trading public research repository (2014–2026 US equities, futures, macro).
Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Status
No open task currently assigned to this session. The working tree should be clean before handoff; verify no half-finished verification artifacts under `experiments/` remain (they are restored by `run_all_verification.py` at completion/restore).

## Immediate Next Task
Resume from the point where the previous session left off. If no task was in flight, begin with a convention-robustness check:

```
SEED=42 bash scripts/check.sh
```

If that passes, proceed to verification per `AGENTS.md` (quick / extended / full). Never leave a verification run half-finished; restore goldens via `SEED=42 python3 run_all_verification.py --restore-only` if interrupted.

## Key Conventions (from AGENTS.md)
- Always run with `SEED=42`.
- `experiments/*.json` are committed golden artifacts — never commit verification output.
- Cache coverage is enforced: pinned inputs under `data/` match SHA-256 in `ledger/data_baseline.json`; run drivers with `QUANT_RESEARCH_OFFLINE=1`.
- `python3 -m py_compile` on changed files (no separate linter).
- Do not commit unless explicitly requested.

## Notes
- Board is shared across peer sessions; post material findings/blockers with `board_post`.
- No CI workflow is present; templates live at `.github/workflow-templates/`.