# Agentic Work Session Handoff

**Timestamp:** 2026-11-18T13:31:27Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** f7f944af4fab898efe030e82ade191f8c74b5bf0 (origin/main, working tree clean at handoff creation)

---

## Initial Task (for the next agentic work session)

This is the durable starting point for the next automated work session. Read this file first, then confirm the environment is intact before making any changes.

**This session's action:** created this timestamped durable handoff and repointed generic handoff aliases to it. No code, experiments, or baselines were modified.

**Next session should:**

1. **Orient.** Skim `AGENTS.md` (commands, conventions, invariants) and `ledger/RESEARCH_LEDGER.md` (experiment ledger, surviving strategies, open items). Research phase is complete for E001–E051; do not re-run the full research program unless a ledger open item explicitly requires it.
2. **Verify integrity before touching anything.** Run the fast offline check:
   ```bash
   SEED=42 bash scripts/check.sh      # or: make check
   ```
   This confirms goldens are clean, the golden baseline matches `ledger/golden_baseline.json`, and data cache coverage holds. If it reports a golden mismatch, restore before committing:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   # or: git checkout <last-good-commit> -- experiments/<file>
   ```
3. **Pick up the highest-priority open item** from `ledger/RESEARCH_LEDGER.md`. Optimizer-determinism (E049/E050) is closed; remaining E030/E041 numeric drift is documented and must **not** be silenced by re-pinning goldens.
4. **Work safely.** Use a branch for changes, keep the committed baseline authoritative, never commit verification output, and never re-pin goldens as a side effect of a verification run.

---

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or: make check

# Quick full verification (~8 min; 8 drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or: make verify-quick

# Extended verification (~21 min; quick + 18 more drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
# or: make verify

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

---

## Critical Integrity Notes

1. **Golden files:** `experiments/*.json` are canonical research artifacts. `run_all_verification.py` backs them up to gitignored `.verify_snapshot/` (with `ACTIVE.json` pid marker) before re-running and restores them afterward — the committed baseline must never be modified by verification.
2. **Baseline integrity:**
   - `scripts/check_goldens_clean.py` fails if a tracked artifact under `experiments/` differs from HEAD or if a stale snapshot is pending.
   - `scripts/check_golden_baseline.py` compares artifacts against SHA-256 hashes pinned in `ledger/golden_baseline.json`. Replacing an artifact requires explicit re-pinning (visible in diff) — **never re-pin as a side effect of running the suite.**
3. **Data/cache coverage:** `scripts/check_data_coverage.py` enforces that every `data.download()` call site resolves to a committed, SHA-256-pinned cache file in `ledger/data_baseline.json`. Unpinned input implies live network download/non-reproducibility. To add data, commit the file and re-pin with `python3 scripts/check_data_coverage.py --update`.
4. **Optimizer determinism (E049/E050, closed):** `src/portfolio_opt.py` validates solver answers against problem constraints (not solver exit status). Residual E041/E042 1-ulp numeric drift is documented; do **not** re-pin those goldens to silence it.

---

## Reproducibility Requirements

- **Seed:** Always `SEED=42`.
- **Convention:** Close-to-close is the v1.2.3 primary convention; overnight decomposition reported alongside every strategy.
- **Data:** Cached parquet in `data/` (gitignored except pinned 2026-10-11/2026-10-12 vintages). E029 fundamentals pinned in `data/fundamentals/`; with `SEED` set, E029 is offline-reproducible.
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional.

---

## Environment Caveat (this runner)

`/usr/bin/python3` (3.12.3) may lack core deps (pandas/numpy/scipy/pyarrow/statsmodels/yfinance). If `scripts/check.sh` fails at pandas-dependent steps, install deps:
```bash
python3 -m pip install -r requirements.txt
```
This is an environment gap, not a code defect.

---

## Handoff Durability

This file is the timestamped durable handoff for this session. Per project convention, mirror it byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` and repoint generic aliases with:
```bash
python3 scripts/repoint_handoff.py handoff_2026-11-18T13-31-27Z_INITIAL_TASK.md
```

---
*Created 2026-11-18T13:31:27Z for durable continuity across agentic work sessions.*
