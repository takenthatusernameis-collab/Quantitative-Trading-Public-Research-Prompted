# Agent Handoff
**Timestamp:** 2026-11-01T13:25:04Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Location:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State
- **Research phase:** Complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` are the committed goldens and must remain untouched by verification runs.
- **Verification:** Snapshot/recovery system in place (`.verify_snapshot/` gitignored). Guards: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` are enforced.
- **Known open items:** E041 numeric drift (133 diffs) due to ill-conditioned QP/optimizer determinism (see ledger E049). Do **not** re-pin to silence it.

## Initial Task For Next Session
**Run a baseline hygiene pass and confirm repo integrity before making any changes.**

### Required Actions (in order)
1. **Check working tree state**
   ```bash
   git status --short
   git log -1 --oneline
   ```

2. **Verify baseline integrity** (fast, offline-safe)
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   This runs: py_compile, golden cleanliness checks, golden baseline fingerprint check, convention robustness, and unit tests.

3. **If checks fail due to a stale/in-progress verification snapshot**
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   SEED=42 bash scripts/check.sh
   ```
   Only restore from `HEAD` or from a commit whose SHA-256 matches `ledger/golden_baseline.json`. Never accept a half-finished verification run.

4. **(Optional but recommended) Quick full verification**
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   Takes ~8 min. Use `--extended` (~21 min) or `--full` (~15 min) only if needed.

## Constraints & Gotchas
- **Always use `SEED=42`** for any run that touches walk-forward/placebo RNG.
- **Never re-pin goldens** as a side effect of running verification. Re-pinning requires explicit justification and `scripts/check_golden_baseline.py --update`.
- **Cache coverage is enforced:** `scripts/check_data_coverage.py` requires all data inputs to exist, be tracked, and match `ledger/data_baseline.json`. Missing inputs will fail (suite runs with `QUANT_RESEARCH_OFFLINE=1`).
- **E041 drift is acceptable:** Extended verification may report 133 numeric diffs for E041; this is known and should not be "fixed" by re-pinning.
- **Conventions:** Close-to-close is primary; overnight decomposition reported. Pre-registration and multiple-testing discipline are non-negotiable.

## Suggested Follow-ups
- Review `ledger/RESEARCH_LEDGER.md` for any items needing attention.
- If modifying code, run `make check` before committing. Never commit verification artifacts.
- If adding new data inputs, commit the files and re-pin via `python3 scripts/check_data_coverage.py --update`.

**End state expected:** `scripts/check.sh` passes with a clean working tree (or only intentional changes). Proceed from there.