# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T04:51:27Z
**Ledger entry**: E667 (durable handoff refresh)
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

---

## Project Status Summary

- **Research phase**: Complete (E001–E043). No open research line.
- **Handoff lineage**: refreshes through E666; this is refresh E667.
- **Validated strategies**: documented in `ledger/RESEARCH_LEDGER.md`.
- **Surviving set**: equity TSM flagship (β-bearing), DN low-beta sort, futures TSM 18m,
  futures realized-roll-yield carry, macro momentum. The market-neutral *total-portfolio*
  blend line is CLOSED (E042/E042b, 4/5).

## State Verified at Handoff Time (2026-11-22T04:51:27Z)

- **HEAD**: `c0112e32597571ea0dc02f5217b0afc8a4fd5631` on `main` == `origin/main`
  (`chore(kilo): checkpoint agent session`, 2026-11-22 04:50:33 +0000).
- **Working tree**: only 12 `__pycache__/*.pyc` bytecode files modified. No source,
  ledger, data, or `experiments/` file is modified. `git diff HEAD -- experiments/` empty.
- **Golden guards** (pure-stdlib, both PASS):
  - `scripts/check_goldens_clean.py` -> ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD
  - `scripts/check_golden_baseline.py` -> ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT
- **No stale verification state**: `.verify_snapshot/` and `.verify_reports/` are absent.
- **Runtime caveat**: `pandas` is NOT installed in this session, so `scripts/check.sh`,
  `make check`, and the experiment drivers could NOT be executed here. Only the two
  stdlib-only golden guards were run. A session with `requirements.txt` installed should
  run the full check (see Initial Task).

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full

# Recover the golden artifacts if a verification run was interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

Install dependencies first if the checks above fail on import:
`pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).

## Critical Integrity Notes (read before running the suite)

1. **Golden files**: `experiments/*.json` are canonical. The verification suite backs them
   up to `.verify_snapshot/` (with an `ACTIVE.json` pid marker) and restores afterward.
   **Never leave a verification run half-finished.** If interrupted, recover with
   `run_all_verification.py --restore-only` (or `git checkout <commit> -- experiments/<file>`
   pinned to the SHA-256 in `ledger/golden_baseline.json`).
2. **Baselines pinned**: SHA-256 fingerprints in `ledger/golden_baseline.json` (goldens) and
   `ledger/data_baseline.json` (data cache). **Do not re-pin** as a side effect of running
   verification — re-pinning belongs in an explicit ledger update, not a re-run.
3. **Data cache**: cached parquet in `data/` (gitignored except pinned 2026-10-12 and
   2026-10-11 vintages + pinned `data/fundamentals/`). Cache coverage is an enforced
   invariant via `scripts/check_data_coverage.py`; the suite runs offline with
   `QUANT_RESEARCH_OFFLINE=1`. A missing cache entry = live yfinance download = not
   bit-reproducible.
4. **Reproducibility**: always `SEED=42`. Close-to-close is the v1.2.3 primary convention;
   overnight decomposition reported alongside. Optimizer answers validate on problem
   constraints, not solver exit status (pinned by `tests/test_portfolio_opt.py`).

## Open Items / Known Drift (from ledger — do not re-pin to silence)

- **E041**: 133 numeric differences remain (1-ulp sensitivity of an ill-conditioned QP).
  Structural differences are gone; decision/gates unchanged. Do NOT re-pin.
- **E030**: 0 differences since 2026-10-20 (16-ETF panel pinned and committed).
- **E029**: fully offline-reproducible (fundamentals snapshot pinned in `data/fundamentals/`).
- **E042/E042b grid artifacts**: still drift 29–133 numeric diffs (1-ulp QP); do not re-pin.
- **Optimizer determinism**: solver exit status is not a validity test — validate on constraints.

## Initial Task for the Next Session

1. Confirm the environment: `pip install -r requirements.txt` if `pandas`/`numpy`/`scipy`
   are missing.
2. Run `SEED=42 bash scripts/check.sh` (fast, offline). It must report a clean,
   convention-robust state and pass the golden guards. If it reports a golden mismatch,
   **stop and restore before doing anything else** (see Integrity Note 1) — do not commit
   a checkpoint that captures verification output as the baseline.
3. If `check.sh` is clean, review `ledger/RESEARCH_LEDGER.md` (tail: E664–E666) and
   `ledger/PRIORITIZATION.md` (active version v1.2.7) for the surviving strategies and the
   standing rules before proposing any new work.
4. The research phase (E001–E043) is closed; any further work should be an explicit,
   pre-registered extension with falsification expectations, not an ad-hoc change. Do not
   move goalposts, do not re-pin baselines, do not commit verification output.

---

*This durable handoff was written at session time 2026-11-22T04:51:27Z. It is mirrored
byte-identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` and the
generic alias pointers are repointed to it. Update/replace with a new timestamped artifact
at the next session boundary.*