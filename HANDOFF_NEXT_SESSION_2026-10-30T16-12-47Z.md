# Agent Handoff — 2026-10-30T17:14:57Z (UTC)

## Current state
- HEAD: 15c1267 chore(kilo): checkpoint agent session
- Working tree: dirty
- Verification snapshot: ACTIVE
- Repo: Quantitative-Trading-Public-Research-Prompted

## Priority task (start here)
Verify baseline integrity before making changes or running verification:
```bash
SEED=42 python3 scripts/check_golden_baseline.py
SEED=42 python3 scripts/check_goldens_clean.py
SEED=42 bash scripts/check.sh
```
If golden checks fail and no live verification is running, recover:
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or: git checkout -- experiments/
```

## Known constraints (do not violate)
- Never leave a verification run half-finished (snapshot in .verify_snapshot/). Always restore if interrupted.
- Do not re-pin goldens to silence numeric drift. E049: optimizer 1-ulp sensitivity remains (E041/E042 drift). Follow ledger guidance.
- Cache coverage enforced (ledger/data_baseline.json). Verification uses QUANT_RESEARCH_OFFLINE=1.
- E029 fundamentals and E030 panel are pinned offline-reproducible. E041 extended drift is an open item.

## Suggested next actions
1. If baselines clean, run quick verification: `SEED=42 make verify-quick` (or `SEED=42 python3 run_all_verification.py`).
2. Review `ledger/RESEARCH_LEDGER.md` for open items before modifying `experiments/` or drivers.
3. If extending verification, note `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` is gitignored reporting only.

## Quick repro
```bash
SEED=42 bash scripts/check.sh        # fast
SEED=42 make verify-quick            # ~8 min
SEED=42 make verify-extended         # ~21 min
SEED=42 make verify-full             # ~15 min
```
