# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T19:25:34Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Git State
- Branch: `main`
- Working tree: clean (`git status` reported no changes)
- Last commit: `3bf7e2b1 chore(kilo): checkpoint agent session`

## Quick Commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Notes
- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are canonical artifacts - never commit verification output
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` if a verification run is interrupted
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Offline mode**: `QUANT_RESEARCH_OFFLINE=1` enforced during verification

## Initial Task
Default: await explicit user instructions. If acting autonomously:
1. Verify working-tree cleanliness against HEAD (`git status`).
2. Run `SEED=42 bash scripts/check.sh` (fast convention-robustness check).
3. If clean, reproduce with `SEED=42 python3 run_all_verification.py --extended` and report any drift; do NOT re-pin goldens.
4. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` before committing anything.

## Last Verification Status
Run `SEED=42 python3 run_all_verification.py --extended` to verify current state.
