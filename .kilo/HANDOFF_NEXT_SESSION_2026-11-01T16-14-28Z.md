# Agent Handoff
**Timestamp:** 2026-11-01T16:14:28Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Location:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State
- **Branch:** `main`, clean working tree. Latest commit: `b0bef31 chore(kilo): checkpoint agent session`.
- **Research phase:** Complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` are committed goldens and must remain untouched by verification runs.
- **Verification:** Snapshot/recovery in `.verify_snapshot/` (gitignored). Guards: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` enforced.
- **Known open items:** E041 numeric drift (133 diffs) due to ill-conditioned QP/optimizer determinism (ledger E049). Do **not** re-pin to silence it.

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
   Runs: py_compile, golden cleanliness, golden baseline fingerprint, convention robustness, unit tests.

3. **If checks fail due to a stale/in-progress verification snapshot**
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   SEED=42 bash scripts/check.sh
   ```
   Restore only from `HEAD` or a commit whose SHA-256 matches `ledger/golden_baseline.json`. Never accept a half-finished verification run.

4. **(Optional but recommended) Quick full verification**
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   ~8 min. Use `--extended` (~21 min) or `--full` (~15 min) only if needed.

## Constraints & Gotchas
- **Always use `SEED=42`** for any run touching walk-forward/placebo RNG.
- **Never re-pin goldens** as a side effect of running verification. Re-pinning needs explicit justification and `scripts/check_golden_baseline.py --update`.
- **Cache coverage enforced:** `scripts/check_data_coverage.py` requires all data inputs tracked and matching `ledger/data_baseline.json`. Suite runs with `QUANT_RESEARCH_OFFLINE=1`; missing cache fails hard.
- **E041 drift is acceptable:** Extended verification may report 133 numeric diffs for E041; known issue, do not fix via re-pinning.
- **Conventions:** Close-to-close primary; overnight decomposition reported. Pre-registration and multiple-testing discipline non-negotiable.

## Suggested Follow-ups
- Review `ledger/RESEARCH_LEDGER.md` for items needing attention.
- If modifying code, run `make check` before committing. Never commit verification artifacts.
- If adding new data inputs, commit files and re-pin via `python3 scripts/check_data_coverage.py --update`.

**End state expected:** `scripts/check.sh` passes with a clean working tree (or only intentional changes). Proceed from there.
