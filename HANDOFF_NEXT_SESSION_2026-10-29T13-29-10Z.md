# HANDOFF - Next Session (2026-10-29T13:29:10Z UTC)

## Goal
Leave a clean, timestamped handoff so the next agent can resume without guessing.

## Current State
- Repo is clean working tree at /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted (git repo).
- Latest commits visible.
- Verification artifacts in experiments/ are canonical goldens; do not overwrite them as a side effect of verification.
- Research phase complete (E001-E043). Surviving validated strategies documented in ledger/RESEARCH_LEDGER.md.

## Immediate Task (Clear Initial Task)
1. **Read AGENTS.md first** to understand project commands, golden baseline rules, verification suite, and reproducibility constraints.
2. **Confirm baseline integrity**: run `make check` (or `SEED=42 bash scripts/check.sh`) to verify goldens are clean vs HEAD and data/ledger baselines match.
3. **Verify current state**: If clean, decide whether to do a quick verification (`make verify-quick`) or skip to targeted work.
4. **Pick next work**: Review `ledger/RESEARCH_LEDGER.md` for any open items (e.g. E041 numeric drift noted as open in ledger; cache coverage etc.) and proceed only if explicitly requested or clearly necessary. Otherwise, follow user's next instruction.

## Important Constraints
- Always use `SEED=42`.
- Do not re-pin goldens to silence numeric drift without following the rules in AGENTS.md (see check_golden_baseline.py / re-pinning policy).
- Verification suite backs up and restores `experiments/` goldens; never leave a verification run half-finished.
- If working tree is dirty due to interrupted verification, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
- Follow project conventions (pre-registration, multiple testing discipline, negative results recorded honestly).
- Prefer fast checks (`make check`) before long runs.

## Quick Commands
```bash
cd /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
SEED=42 bash scripts/check.sh        # fast checks
SEED=42 python3 run_all_verification.py --quick  # quick verify (~8 min)
git status --short
```

## Context Files
- `AGENTS.md` - commands, rules, verification
- `ledger/RESEARCH_LEDGER.md` - research state
- `run_all_verification.py` - verification entrypoint
- `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`

## Notes
- This handoff is durable and timestamped. The symlink `HANDOFF.md` may point to the most recent one.
