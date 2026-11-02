# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-11-02T18:39:04Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**State:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Current State Summary

- **Canonical artifacts:** `experiments/*.json` are the committed goldens. The verification suite backs them up to gitignored `.verify_snapshot/` (with `ACTIVE.json` holding owning PID) and restores them afterwards — never leave a verification run half-finished.
- **Integrity guards (must pass before changes):** `scripts/check_goldens_clean.py` (working tree vs HEAD), `scripts/check_golden_baseline.py` (artifacts vs `ledger/golden_baseline.json` SHA-256s), `scripts/check_data_coverage.py` (every `data.download()` call site has a pinned, git-tracked cache entry). All three run as part of `scripts/check.sh`.
- **Data:** `data/` is mostly gitignored except pinned vintages. `data/vintages.json` pins 2026-10-12; 2026-10-11 is committed (used by E026/E028/E029/E030/E034/E036/E037). Fundamentals for E029 are pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` (offline-reproducible with `SEED=42`). Cache coverage is enforced.
- **Known drift (do not silence):** Optimizer determinism issue (E049). Ill-conditioned tangency QP causes numeric drift in E041/E042 grid artifacts (1-ulp sensitivity). SLSQP status 8 is not gated (fixed). Do **not** re-pin goldens to hide this drift.
- **Verification modes:** `check` (~seconds), `verify-quick` (~8 min), `verify-extended` (~21 min), `verify-full` (~15 min). `--skip-slow` skips batch/regression; `--restore-only` recovers goldens after interruption.

## Initial Task (Clear & Actionable)

**Primary objective:** Ensure repo integrity is clean before doing any work. Do not modify canonical golden artifacts.

1. **Verify integrity (required):**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   This runs py_compile, template validation, convention robustness, golden cleanliness vs HEAD, golden baseline SHA-256 checks, data coverage, and portfolio optimizer tests.

2. **If `check.sh` reports golden mismatches:**
   - If a verification run was interrupted, restore: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
   - If HEAD already contains a captured run, restore pinned artifacts from the last commit whose SHA-256 matches `ledger/golden_baseline.json` (e.g. `git checkout <commit> -- experiments/<file>`). See AGENTS.md warnings about past incidents.
   - Re-run `SEED=42 bash scripts/check.sh` until clean.

3. **Only proceed with user-requested changes after step 1 passes.**
   - If the user has no specific task, answer questions using existing artifacts (`ledger/RESEARCH_LEDGER.md`, `experiments/*.json`, `docs/`).
   - Do **not** run the full verification suite unless explicitly requested. It overwrites and restores goldens by design.
   - Never re-pin `ledger/golden_baseline.json` or artifacts as a side effect of running verification.

## Key References
- `AGENTS.md` — full commands, conventions, guards, warnings
- `ledger/RESEARCH_LEDGER.md` — research history and dispositions
- `ledger/golden_baseline.json` — pinned SHA-256s for canonical artifacts
- `ledger/data_baseline.json` — pinned SHA-256s for required data caches

## Quick Recovery Commands
```bash
# Check integrity
SEED=42 bash scripts/check.sh

# Restore goldens after interruption
SEED=42 python3 run_all_verification.py --restore-only

# Quick reproduction check (8 drivers)
SEED=42 python3 run_all_verification.py
```