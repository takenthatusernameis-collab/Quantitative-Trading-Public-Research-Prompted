# INITIAL TASK - Handoff for Next Agent Session
Timestamp (UTC): 2026-11-03T17:16:17Z
Repository: Quantitative-Trading-Public-Research-Prompted
Branch/HEAD: $(git rev-parse --short HEAD)
Working Directory: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Goal
Continue quantitative strategy research per AGENTS.md. Research phase is complete (E001–E043); surviving validated strategies documented in ledger/RESEARCH_LEDGER.md.

## Current State
- Repo in clean, checkpointed state (chore(kilo): checkpoint agent session)
- Golden artifacts in experiments/ committed and protected
- Verification suite is the gate (check.sh / run_all_verification.py)
- Critical invariants: never leave verification run half-finished; restore experiments/ if interrupted; follow golden baseline rules

## Immediate Priorities
1. Verify repo state - check for active verification runs or dirty experiments/
   - Run: `SEED=42 python3 run_all_verification.py --restore-only` if needed
   - Or check for `.verify_snapshot/ACTIVE.json`
2. Understand current research status - read ledger/RESEARCH_LEDGER.md and AGENTS.md
3. Follow verification discipline - use SEED=42; never re-pin goldens as side effect

## Quick Commands
```bash
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Notes
- E029, E030 offline-reproducible since 2026-10-20 (data pinned)
- E041 has remaining numeric drift (1-ulp sensitivity) - do not re-pin
- Optimizer validates on constraints not solver exit status
- Cache coverage enforced - new data.download() needs cache + ledger entry

## Handoff Message
Repository is clean and checkpointed. Pick up from understanding the ledger and current state. Follow all baseline integrity rules strictly.
