# HANDOFF_NEXT_SESSION_2026-10-30T03-32-57Z

**Timestamp:** 2026-10-30T03:32:57Z (UTC)
**Branch:** main

## ⚠️ INITIAL TASK — INTEGRITY CHECK FAILED (do this first)

`SEED=42 bash scripts/check.sh` fails at step 3 (pinned baseline guard): two artifacts
drifted by 1-ULP on `corr_spy`:
- `experiments/blend_tsm_dnlowbeta_large_liquid.json`
- `experiments/pairs_large_liquid.json`

Root cause: checkpoint commit `ee6998d` captured verification output, silently replacing
the canonical baseline pinned in `49aebd5`. Recovery already performed: both files restored
from `49aebd5` to pinned SHA-256. Baseline guard now passes; only `check_goldens_clean.py`
(working tree vs HEAD) still fails because HEAD is the drifting checkpoint.

### Recovery action required
Commit the restore to clear `check_goldens_clean.py`:
```
git add experiments/blend_tsm_dnlowbeta_large_liquid.json experiments/pairs_large_liquid.json
git commit -m "restore: revert 1-ULP drift captured in checkpoint commit ee6998d; matches ledger/golden_baseline.json"
```
Then confirm with `SEED=42 bash scripts/check.sh`.

### If the drift is actually intended
Re-pin deliberately with `python3 scripts/check_golden_baseline.py --update` and record
the reason. Do not re-pin as a side effect of running the verification suite.

## Initial Task For Next Session
1. Commit the baseline restore above; confirm `SEED=42 bash scripts/check.sh` passes.
2. Review `ledger/RESEARCH_LEDGER.md` open items, especially E049 (do not re-pin E041/E042
   grid artifacts to silence drift).
3. No new feature/fix requested. Treat integrity restoration as the initial task.
   If a new request arrives on resume, satisfy it while respecting AGENTS.md guardrails.

## Quick Commands
```
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --restore-only
```

## Guardrails
- Never leave a verification run half-finished; restore before committing.
- Never re-pin goldens as a side effect of the verification suite.
- Respect data coverage; unpinned inputs fail in offline verification (QUANT_RESEARCH_OFFLINE=1).
- Follow AGENTS.md: SEED=42, pre-registration, no moving goalposts, honest negative results.
