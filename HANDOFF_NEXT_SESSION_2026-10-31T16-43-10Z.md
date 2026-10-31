# HANDOFF - Next Agentic Session (2026-10-31T16:43:10Z)

## State Summary
- **Phase**: Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baselines**: `experiments/*.json` are canonical goldens (committed). Verification suite backs up/restores them.
- **Guards in place**: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, optimizer determinism fix + tests (`tests/test_portfolio_opt.py`).
- **Pinned data**: `data/vintages.json` (2026-10-12), separate vintage (2026-10-11) for E026/E028/E029/E030/E034/E036/E037, fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` (E029 offline reproducible), E030 panel committed.
- **Known drift**: E041/E042 grid show 1-ulp optimizer sensitivity (133 numeric diffs remaining); not to be re-pinned. E030/E029 now reproduce with 0 diffs.

## Initial Task (Clear, Actionable)
**Goal**: Verify baseline integrity and establish a clean starting state before any new work.

1. **Check goldens & snapshots**
   ```bash
   SEED=42 python3 scripts/check_goldens_clean.py
   SEED=42 python3 scripts/check_golden_baseline.py
   ```
   - Must pass. If stale snapshot exists or goldens differ from HEAD/ledger, recover before proceeding (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` as appropriate).

2. **Check data coverage (offline invariant)**
   ```bash
   SEED=42 python3 scripts/check_data_coverage.py
   ```
   - All driver data inputs must exist, be git-tracked, and match `ledger/data_baseline.json`.

3. **Quick verification (fast sanity)**
   ```bash
   SEED=42 make check
   ```
   or
   ```bash
   SEED=42 python3 run_all_verification.py --skip-slow
   ```
   - Should pass with goldens unchanged.

4. **Review open items**
   - Read `ledger/RESEARCH_LEDGER.md` sections for E049 (optimizer determinism), E048 (data coverage), E045 (E029), E030 status.
   - Note: do **not** re-pin goldens to silence optimizer drift; follow ledger guidance.

## Guardrails (Must Follow)
- **Never leave verification half-finished**: if interrupted, recover via `--restore-only` or `git checkout -- experiments/`. Snapshot lives in `.verify_snapshot/` with `ACTIVE.json`.
- **Golden integrity**: replacing artifacts requires re-pinning via `scripts/check_golden_baseline.py --update` and explicit justification in diff/ledger. Do not re-pin as side effect of verification.
- **Offline reproducibility**: use `QUANT_RESEARCH_OFFLINE=1` behavior (verification does this). Missing caches are hard failures.
- **Convention**: close-to-close v1.2.3 primary; overnight reported.
- **No commits of verification output** unless explicitly requested.
- **Determinism**: always use `SEED=42`.

## Quick Reference
- Full docs: `AGENTS.md`
- Verification: `run_all_verification.py` (`--quick` default in quick verify, `--extended`, `--full`)
- Individual: `src/batch_run.py`, `src/validate.py`, `experiments/run_e*.py`
- Tests/guards run via `scripts/check.sh`

## Next Agent Instructions
Start with steps 1-3 above. If all pass, report clean state and await user direction. If any guard fails, fix per recovery rules before making other changes. Do not modify `experiments/*.json` without following the golden baseline update procedure.
