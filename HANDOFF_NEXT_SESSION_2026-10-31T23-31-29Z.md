# Handoff - 2026-10-31T23:31:29Z

## Initial task for next session
Run `SEED=42 bash scripts/check.sh` and confirm golden integrity passes cleanly; if any stale snapshot exists, recover first with `SEED=42 python3 run_all_verification.py --restore-only`. Do not modify experiments/*.json.

## Quick verification commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
```
