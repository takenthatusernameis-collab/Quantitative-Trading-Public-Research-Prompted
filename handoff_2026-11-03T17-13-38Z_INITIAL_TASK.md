# INITIAL TASK - Handoff for Next Agent Session
Timestamp (UTC): 2026-11-03T17:13:38Z
Repository: Quantitative-Trading-Public-Research-Prompted
Branch/HEAD: $(git rev-parse --short HEAD)
Working Directory: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Goal
Continue quantitative strategy research per AGENTS.md. Research phase is complete (E001–E043); surviving validated strategies documented in ledger/RESEARCH_LEDGER.md.

## Current State
- Recent commits show checkpoint sessions (chore(kilo): checkpoint agent session)
- All golden artifacts in experiments/ are committed and protected
- Verification suite is the gate (check.sh / run_all_verification.py)
- Critical invariants: never leave verification run half-finished, restore experiments/ if interrupted, follow golden baseline rules

## Immediate Priorities
1. **Verify repo state** - Check for any in-progress verification runs or dirty experiments/
   - Run: `SEED=42 python3 run_all_verification.py --restore-only` if needed
   - Or check for `.verify_snapshot/ACTIVE.json`

2. **Understand current research status** - Read key docs
   - `ledger/RESEARCH_LEDGER.md` - decisions on all experiments
   - `AGENTS.md` - full conventions and commands
   - Look for any TODO/FIXME or open items

3. **Follow verification discipline**
   - Before making changes, understand if changes affect goldens
   - Never re-pin goldens as side effect of verification
   - Use `SEED=42` for reproducibility
   - Run `make check` or appropriate verify target after changes

## Quick Commands
```bash
# Check for active verification
ls -la .verify_snapshot/ 2>&1 | head

# Verify clean state
SEED=42 bash scripts/check.sh

# See ledger
cat ledger/RESEARCH_LEDGER.md | head -200
```

## Notes
- E029, E030 offline-reproducible since 2026-10-20 (data pinned)
- E041 has remaining numeric drift due to ill-conditioned QP (1-ulp sensitivity) - do not re-pin to silence
- Optimizer validates on constraints not solver exit status (per tests/test_portfolio_opt.py)
- Cache coverage enforced - any new data.download() needs cache + ledger entry

## Handoff Message
The research repository is in a clean, checkpointed state. Pick up from understanding the ledger and current state. Follow all baseline integrity rules strictly. Any verification must complete fully or be restored.

(End of file)
