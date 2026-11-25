# Handoff — Next Agentic Work Session (INITIAL TASK)

**Timestamp**: 2026-11-25T09:13:01Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Git HEAD**: 7b2a4dec (chore(kilo): checkpoint agent session)
**Working tree**: clean (no staged/unstaged changes)

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase is COMPLETE (E001–E043). Surviving
validated strategies and all negative results are recorded in
`ledger/RESEARCH_LEDGER.md`. `experiments/*.json` are the committed golden
artifacts and must never be overwritten by verification output.

## INITIAL TASK (do this first)
1. Run the fast integrity gate and confirm a clean baseline before anything else:
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - Must report goldens clean (no mismatch vs HEAD, no stale `.verify_snapshot/`).
   - If it reports a golden mismatch: DO NOT commit. Restore the pinned artifact
     (`git checkout <commit> -- experiments/<file>` where `<commit>` matches
     `ledger/golden_baseline.json`), or `SEED=42 python3 run_all_verification.py --restore-only`.
2. Confirm `git status` is clean and HEAD is unchanged. Report the check.sh result.
3. Only after a clean gate: await/accept a new research task. Do NOT start a
   verification run that overwrites goldens unless the task explicitly requires it,
   and never leave one half-finished.

## Quick Commands
```bash
SEED=42 bash scripts/check.sh                              # fast convention + template + golden checks
SEED=42 python3 run_all_verification.py                    # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended         # +18 more drivers (~21 min)
SEED=42 python3 run_all_verification.py --full             # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 verify_convention_robustness.py            # convention only, no writes
SEED=42 python3 run_all_verification.py --restore-only     # recover goldens after interruption
```

## Key Notes / Guardrails
- **Seed**: always `SEED=42` (walk-forward + placebo RNG).
- **Golden files**: `experiments/*.json` are canonical; verification backs them up
  and restores them. Never commit verification output. A checkpoint commit that
  captures a re-run silently replaces the baseline.
- **Baseline integrity**: `scripts/check_goldens_clean.py` +
  `scripts/check_golden_baseline.py` (both first-class in `scripts/check.sh`)
  compare the tree and every tracked artifact against `ledger/golden_baseline.json`
  SHA-256 pins. Re-pin only for a deliberate, ledger-recorded change — never as a
  side effect of a verification run.
- **Data**: cached parquet in `data/` (gitignored except pinned 2026-10-12 and
  2026-10-11 vintages; E029 fundamentals pinned in `data/fundamentals/`). Cache
  coverage is an enforced invariant (`scripts/check_data_coverage.py`).
- **Offline mode**: verification runs with `QUANT_RESEARCH_OFFLINE=1`; a missing
  cache entry fails hard instead of downloading (yfinance is not bit-reproducible).
- **Conventions**: close-to-close is the v1.2.3 primary; overnight reported alongside.
- **Lint**: no separate linter; run `python3 -m py_compile` on changed files.

## Current Status
No active verification run. Repository is clean and at a known-good checkpoint.
Research phase complete; next session starts from the INITIAL TASK above.
