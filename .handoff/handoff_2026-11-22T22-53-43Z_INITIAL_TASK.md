# Initial Task Message — Next Agentic Work Session

**Timestamp**: 2026-11-22T22:53:43Z
**Repo HEAD**: `89492674e16bc3f6362d39766eeacf550a3004b7` (main == origin/main)
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## Read this first — do NOT do another handoff-only refresh

The repository's research phase is **complete** (E001–E043; survivors in
`ledger/RESEARCH_LEDGER.md`). Thousands of handoff files already exist; adding
yet another handoff as your only deliverable is negative value. **Your job is
real work, not another handoff.** If you finish this session having only added
a handoff file, you have failed.

Do NOT append an "ENNN — Durable handoff refresh" entry to the ledger as your
deliverable. If you have nothing real to do, say so and stop.

---

## Verified state at the moment this file was written (22:53:43Z)

- `git status` clean; `git diff HEAD -- experiments/` empty; `.verify_snapshot/`
  and `.verify_reports/` absent.
- `main == origin/main` (`git rev-list --left-right --count origin/main...HEAD`
  = `0  0`).
- **All real (non-test) integrity checks PASS** on this HEAD. `scripts/check.sh`
  clears these before it stops: `check_json_artifacts.py`, `check_goldens_clean.py`,
  `check_golden_baseline.py` (107 baseline fingerprints match),
  `check_data_coverage.py` (all 35 pinned data inputs present, tracked, unchanged).
- **`scripts/check.sh` exits non-zero for one environmental reason only**:
  `python3 -m unittest tests.test_data_coverage` reports `FAILED (errors=3)`,
  each `ModuleNotFoundError: No module named 'pandas'`; `set -e` then aborts
  before the remaining steps. Missing-dependency problem, NOT a data/golden
  integrity problem.
- **Dependencies are NOT provisioned** this session (`import numpy`/`pandas` fail).
  Install with `pip install -r requirements.txt`, then re-run `scripts/check.sh`;
  it should reach `=== All checks passed ===`.

---

## Initial task (do these in order)

1. **Provision and run the fast gate.**
   ```bash
   pip install -r requirements.txt
   SEED=42 bash scripts/check.sh   # or: make check
   ```
   Confirm it ends with `=== All checks passed ===`.

2. **Run the quick reproducibility suite and confirm the baseline is intact.**
   ```bash
   SEED=42 python3 run_all_verification.py   # verify-quick (~8 min)
   ```
   The suite backs up and restores `experiments/*.json` itself. If interrupted,
   recover with `SEED=42 python3 run_all_verification.py --restore-only`
   (or `git checkout -- experiments/`). Never commit verification output.

3. **Address the one real open technical item (ledger E049): E041/E042
   ill-conditioned-QP drift.** The tangency QP in `src/portfolio_opt.py` still
   moves `min_var` answers by ~1e-05 under a 1-ulp input perturbation, so E041
   (133 numeric diffs) and E042 grid artifacts exceed the 1e-4 tolerance and
   show as drifting in the `--extended` report.
   - Do **not** silence this by re-pinning the golden; the committed golden is
     authoritative, not the latest re-run.
   - The pinned rule from E049 — validate the solver answer on the problem's
     constraints, not the solver exit status — is guarded by
     `tests/test_portfolio_opt.py`. Any fix must keep that test green.
   - A legitimate improvement is conditioning/regularization of the QP or a
     deterministic tie-break, with the effect on E041's 133 diffs and E042's
     grid quantified and recorded honestly.

4. **Do not add a new research experiment casually.** Any new experiment must
   follow pre-registration (gates, falsification expectations, sensitivity grid)
   before it runs, per `AGENTS.md` and `ledger/PRIORITIZATION.md`.

---

## If you genuinely have nothing to do

Do **not** fabricate work and do **not** refresh the handoff. Instead do one
concrete cleanup that reduces this repo's churn: propose (do not silently
execute) a `.gitignore` + `git rm --cached` plan for the historical
`handoff_*` / `HANDOFF-*` / `HANDOFF_*` files, keeping only a single
`HANDOFF.md` and the `ledger/`. That is real, reviewable work.

---

## Reference: key commands

| Purpose | Command |
|---|---|
| Fast gate (seconds, offline) | `SEED=42 bash scripts/check.sh` |
| Quick verification (~8 min) | `SEED=42 python3 run_all_verification.py` |
| Extended (+18 drivers, ~21 min) | `SEED=42 python3 run_all_verification.py --extended` |
| Full (E042 n_sim=50 + grid, ~15 min) | `SEED=42 python3 run_all_verification.py --full` |
| Recover after interrupted run | `SEED=42 python3 run_all_verification.py --restore-only` |

- **Seed**: always `SEED=42`.
- Never re-pin goldens/data as a side effect of a run; never commit verification
  output; never claim a golden mismatch is fixed by re-pinning.
