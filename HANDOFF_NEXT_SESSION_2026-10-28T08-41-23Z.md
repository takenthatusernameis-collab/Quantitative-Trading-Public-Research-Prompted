# HANDOFF — Timestamped initial task for next agentic session

Timestamp (UTC): 2026-10-28T08-41-23Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: 23e068821371b9ec5e194f8e331e28d4b98b9e37
Working tree: only `__pycache__/*.pyc` (gitignored noise) — no tracked changes
Verify snapshot: none

## Mission for next session
Start here and verify baseline integrity before making any changes. Research phase complete (E001–E043); surviving validated strategies in `ledger/RESEARCH_LEDGER.md`. No new research warranted unless explicitly requested.

## Immediate priorities (do in order)
1. `git status --short` — confirm only `__pycache__/*.pyc` noise; no tracked diffs.
2. `SEED=42 bash scripts/check.sh` — must pass (convention-robustness + template validation + golden/data/coverage guards).
3. If check passes, run verification at chosen scope:
   - Quick (~8 min): `SEED=42 python3 run_all_verification.py`
   - Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended` (E041 numeric drift expected; do NOT re-pin)
4. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`); confirm `.verify_snapshot/ACTIVE.json` removed.

## Known open items
- E041: ~133 numeric diffs (1-ulp QP sensitivity); structural diffs resolved. Do not re-pin.
- E030/E029: offline-reproducible via pinned inputs; do not revert to live yfinance.
- Data coverage: any new `data.download()` inputs must be committed + re-pinned via `scripts/check_data_coverage.py --update`.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`).

## Suggested first command
```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```

## Current handoff pointer
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-28T08-41-23Z.md`
(End of file)
