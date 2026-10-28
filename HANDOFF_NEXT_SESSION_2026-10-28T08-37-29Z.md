# Handoff for Next Agentic Session
Timestamp (UTC): 2026-10-28T08:37:29Z
Repo: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
Branch/HEAD: main (see `git status`)
Verify snapshot: none active (`.verify_snapshot/ACTIVE.json` absent)

## Initial Task for Next Session
1. Read `AGENTS.md` fully (baseline integrity + reproducibility rules).
2. Run `git status --short` to confirm clean working tree.
3. Run `SEED=42 bash scripts/check.sh` (must pass before any changes).
4. If clean, perform a quick reproducibility sanity check: `SEED=42 python3 run_all_verification.py` (do not re-pin goldens; follow AGENTS.md).
5. If interrupted/modified goldens: recover with `SEED=42 python3 run_all_verification.py --restore-only`, then re-run check.

## Key Constraints
- Always use SEED=42.
- Never re-pin `experiments/*.json` or data baselines as a side effect of verification.
- E041 numeric drift (133 diffs) is an open item; do not silence by re-pinning.
- Do not commit unless explicitly asked.

## Quick Commands
- Check: `SEED=42 bash scripts/check.sh` / `make check`
- Quick verify: `SEED=42 python3 run_all_verification.py` / `make verify-quick`
- Restore only: `SEED=42 python3 run_all_verification.py --restore-only`

## Handoff pointer
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-28T08-37-29Z.md` (see also `HANDOFF_NEXT.md`).
