# HANDOFF_NEXT_SESSION — 2026-10-28T08:38:17Z

## Status
- **Research phase:** Complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Working tree:** Clean checkpoint from recent session (`git log --oneline -1` shows `6cf68a5 chore(kilo): checkpoint agent session`).
- **Golden baseline:** All `experiments/*.json` are canonical (pinned in `ledger/golden_baseline.json`). Verification suite restores them after runs.
- **Verification health:** `scripts/check.sh` and guards (`check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`) are in place.

## Initial Task (clear, actionable)
**Goal:** Ensure baseline integrity and run a fast verification pass to confirm the repo is in a known-good state before any new experimentation.

**Steps (do in order):**
1. **Verify clean state**
   - `git status --short` (should be clean or only expected artifacts)
   - `SEED=42 python3 scripts/check_goldens_clean.py` (must pass; if it reports "live verification" that’s okay, else fix before committing)
   - `SEED=42 python3 scripts/check_golden_baseline.py` (must pass against `ledger/golden_baseline.json`)

2. **Quick convention + sanity checks**
   - `SEED=42 bash scripts/check.sh` (fast: convention robustness + template validation). Should pass.

3. **Quick verification (reproducibility smoke)**
   - `SEED=42 python3 run_all_verification.py` (quick; ~8 min). This re-runs the 8 drivers (E012, E023, E024 --merge, E027, E035, E037, E039, E042-lead), runs batch_run/validate, and checks extended bits.
   - If it reports drift, **do not re-pin goldens**. Read `ledger/RESEARCH_LEDGER.md` entries (notably E049, E048, E045) for context on known acceptable drift vs structural issues.

4. **Report state**
   - Summarize pass/fail of steps 1-3. If all green, repo is ready for new work. If any guard fails, stop and fix per AGENTS.md before proceeding.

## Key Constraints (must follow)
- **Never leave verification half-finished.** If you start `run_all_verification.py`, let it complete or use `--restore-only`. Backup lives in `.verify_snapshot/` with `ACTIVE.json`.
- **Goldens are canonical.** Do not modify `experiments/*.json` as a side effect of verification. Re-pinning requires explicit justification and `--update` on the relevant guard with diff review.
- **Data coverage enforced.** Any new data input must be committed and re-pinned via `scripts/check_data_coverage.py --update`.
- **Optimizer determinism:** SLSQP status 8 can be acceptable if feasible/optimal; validation is against problem constraints. Known small numeric drift in E041/E042 grids is acceptable per ledger (do not silence by re-pinning).
- **Seeds:** Always use `SEED=42`.
- **Offline reproducibility:** Verification runs with `QUANT_RESEARCH_OFFLINE=1`; missing caches fail hard.

## Quick References
- `ledger/RESEARCH_LEDGER.md` — disposition of E001–E049
- `ledger/golden_baseline.json` — pinned SHA-256s for `experiments/*.json`
- `ledger/data_baseline.json` — pinned SHA-256s for cached inputs
- `AGENTS.md` — full commands, baseline integrity, and reproducibility notes
- `run_all_verification.py` — `--quick`, `--extended`, `--full`, `--skip-slow`, `--restore-only`

## Suggested First Message to Next Agent
> "Repo checkpoint at 6cf68a5. Run baseline integrity checks (check_goldens_clean, check_golden_baseline, check_data_coverage) then `SEED=42 bash scripts/check.sh` followed by `SEED=42 python3 run_all_verification.py` (quick). Report pass/fail and any drift with references to ledger entries. Do not re-pin goldens."
