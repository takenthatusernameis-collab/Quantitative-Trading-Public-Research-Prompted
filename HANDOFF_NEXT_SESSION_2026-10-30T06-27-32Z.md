# HANDOFF — 2026-10-30T06-27-32Z

## Initial Task
**Verify baseline integrity and confirm the verification suite is clean before making any changes.**

## Context
- Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts live in `experiments/*.json` (golden baselines). The verification suite backs these up to `.verify_snapshot/`, re-runs drivers, and restores them afterwards — never leave a verification run half-finished.
- Known open items (do not re-pin to silence):
  - E041: 133 numeric diffs remain due to ill-conditioned QP sensitivity (optimizer determinism fixed; 3 structural diffs eliminated). Reported in extended summary only.
  - E042/E041 grid can drift by 1-ulp; do not re-pin artifacts to mask this.

## Required Steps (in order)
1. **Check integrity first**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Must pass: goldens clean vs HEAD, baseline pinned in `ledger/golden_baseline.json`, data coverage pinned in `ledger/data_baseline.json`, and tests pass.

2. **Run full verification**
   ```bash
   SEED=42 python3 run_all_verification.py --full
   ```
   This runs E042 with `n_sim=50` and the 96-config sensitivity grid. Expect only reporting drift (E041) in extended summary.

3. **Inspect reports if needed**
   - `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored, reporting only)
   - `ledger/RESEARCH_LEDGER.md` for context on open items

## Recovery
If interrupted or `check.sh` reports a pending snapshot:
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or: git checkout -- experiments/
```
If HEAD already contains a bad commit, restore from the last commit matching `ledger/golden_baseline.json` via `git checkout <commit> -- experiments/<file>`.

## Read First
- `AGENTS.md` — commands, conventions, reproducibility rules
- `ledger/RESEARCH_LEDGER.md` — current disposition of all experiments
- `ledger/golden_baseline.json` and `ledger/data_baseline.json`

## Rules
- Never commit verification output. Restore before committing.
- Do not re-pin goldens/data as a side effect of the verification suite. Only re-pin via explicit `--update` flags on the guard scripts.
- Re-execute with `QUANT_RESEARCH_OFFLINE=1` is enforced by the suite; all required caches must be present and pinned.
