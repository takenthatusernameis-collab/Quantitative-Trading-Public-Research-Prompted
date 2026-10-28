# HANDOFF_NEXT_SESSION_2026-10-28T13-33-24Z

## Initial Task (for next agent)
**Verify baseline integrity and confirm clean verification state before making any changes.**

The verification suite can overwrite `experiments/*.json` while running and restores them afterward; a half-finished run or a silently re-pinned golden will corrupt the canonical record. Treat the committed artifacts as authoritative.

## Immediate Actions (in order)
1. **Check repo state**
   ```bash
   git status --short
   git log -1 --oneline
   ```

2. **Run fast integrity checks**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   This runs `check_goldens_clean.py` (working tree vs HEAD), `check_golden_baseline.py` (vs pinned SHA-256 in `ledger/golden_baseline.json`), `check_data_coverage.py`, py_compile, and unit tests.

3. **If checks fail**
   - If a verification run was interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`). Do **not** commit verification output.
   - If golden baseline drift is reported but not from a live run: restore to the last commit matching `ledger/golden_baseline.json` (see AGENTS.md). Never re-pin baselines as a side effect of verification.
   - If data coverage fails: commit missing tracked caches and re-pin with `python3 scripts/check_data_coverage.py --update` only if intentionally adding inputs.

4. **If checks pass**
   - Run quick verification if you need to validate drivers: `SEED=42 python3 run_all_verification.py` (~8 min)
   - Or extended/full only if explicitly requested. See AGENTS.md for modes.

## Critical Constraints
- **Canonical baselines**: `experiments/*.json` are committed goldens. Verification backs up to `.verify_snapshot/` (gitignored) with `ACTIVE.json` and restores after. Never leave a run half-finished.
- **No silent re-pinning**: `ledger/golden_baseline.json` and `ledger/data_baseline.json` are the authority. Re-pinning requires explicit intent and will show in diff.
- **Offline reproducibility**: E029 uses pinned fundamentals (`data/fundamentals/`), E030 uses pinned 16-ETF panel, vintage dates are pinned (`data/vintages.json`). `QUANT_RESEARCH_OFFLINE=1` is used by verification.
- **Known drift (do not silence)**: E041 has optimizer-induced numeric drift (ill-conditioned QP); E042 lead artifacts may drift slightly across builds. See AGENTS.md "Optimizer determinism" and ledger E049. Do not re-pin to hide this.
- **Pre-registration discipline**: Goalposts never moved post-hoc. Sensitivity grids reported, not gated. Negative results recorded as REJECTED/PARTIAL.

## Key References
- `AGENTS.md` - full commands, guards, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` - research status (E001–E043 complete)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `run_all_verification.py`, `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`

## Notes
- Research phase is complete. Surviving strategies documented in the ledger. Avoid expanding scope beyond what's explicitly requested.
- If multiple handoffs exist, this is the most recent timestamped one for the next session.
