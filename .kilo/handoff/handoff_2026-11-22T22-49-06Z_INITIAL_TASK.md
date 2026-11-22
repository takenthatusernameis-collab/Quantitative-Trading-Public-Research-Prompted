# Initial Task Message — Next Agentic Work Session

**Timestamp**: 2026-11-22T22:49:06Z
**Repo HEAD**: `89492674e16bc3f6362d39766eeacf550a3004b7` (main == origin/main)
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## Read this first — do NOT do another handoff-only refresh

This repository's research phase is **complete** (E001–E043; survivors in
`ledger/RESEARCH_LEDGER.md`). Sessions E652–E713+ have each done nothing except
leave a new handoff and append a "Durable handoff refresh" ledger entry. That
loop is the problem, not the task. **Your job is real work, not another
handoff.** If you finish this session having only added a handoff file, you have
failed.

Concretely: do NOT append an "ENNN — Durable handoff refresh" entry to the
ledger as your deliverable. The repo already tracks **8,000+ handoff files**;
adding one more is negative value. If you have nothing real to do, say so and
stop — do not fabricate a handoff refresh.

---

## Verified state at the moment this file was written (22:49:06Z)

- `git status` clean; `git diff HEAD -- experiments/` empty; `.verify_snapshot/`
  and `.verify_reports/` absent.
- `main == origin/main` (`git rev-list --left-right --count origin/main...HEAD`
  = `0  0`).
- **All real (non-test) integrity checks PASS** on this HEAD. `scripts/check.sh`
  clears these before it stops: `check_json_artifacts.py` (all committed JSON
  parses), `check_goldens_clean.py` (goldens match HEAD),
  `check_golden_baseline.py` (107 baseline fingerprints match),
  `check_data_coverage.py` (all 35 pinned data inputs present, tracked, unchanged).
- **`scripts/check.sh` exits non-zero for one environmental reason only**:
  `python3 -m unittest tests.test_data_coverage` reports `FAILED (errors=3)`,
  each `ModuleNotFoundError: No module named 'pandas'`; `set -e` then aborts the
  script before the remaining steps. This is a missing-dependency problem, NOT a
  data/golden integrity problem.
- **Dependencies are NOT provisioned** this session (`import numpy`/`pandas`
  fail). Install with `pip install -r requirements.txt`, then re-run
  `scripts/check.sh`; it should reach `=== All checks passed ===`.

---

## Initial task (do these in order)

1. **Provision and run the fast gate.**
   ```bash
   pip install -r requirements.txt
   SEED=42 bash scripts/check.sh      # or: make check
   ```
   Confirm it ends with `=== All checks passed ===`.

2. **Run the quick reproducibility suite and confirm the baseline is intact.**
   ```bash
   SEED=42 python3 run_all_verification.py            # verify-quick (~8 min)
   ```
   The suite backs up and restores `experiments/*.json` itself. If it is ever
   interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`
   (or `git checkout -- experiments/`). Never commit verification output.

3. **Address the one real open technical item (ledger E049): E041/E042
   ill-conditioned-QP drift.** The tangency QP in `src/portfolio_opt.py` still
   moves `min_var` answers by ~1e-05 under a 1-ulp input perturbation, so the
   E041 (133 numeric diffs) and E042 grid artifacts still exceed the 1e-4
   comparison tolerance and show up as drifting in the `--extended` report.
   - Do **not** silence this by re-pinning the golden (the ledger's standing
     disposition is that the committed golden is authoritative, not the latest
     re-run).
   - The pinned rule from E049 — validate the solver answer on the problem's
     constraints, not the solver exit status — is guarded by
     `tests/test_portfolio_opt.py`. Any fix must keep that test green.
   - A legitimate improvement is conditioning/regularization of the QP or a
     deterministic tie-break, with the effect on E041's 133 diffs and E042's
     grid quantified and recorded honestly.

4. **Do not add a new research experiment casually.** Any new experiment must
   follow the pre-registration protocol (gates, falsification expectations,
   sensitivity grid) before it is run, per `AGENTS.md` and
   `ledger/PRIORITIZATION.md`.

---

## If you genuinely have nothing to do

Do **not** fabricate work and do **not** refresh the handoff. Instead, do one
concrete cleanup that reduces the churn this repo is drowning in:

- The handoff aliases (`handoff_NEXT`, `handoff_LATEST`, `handoff_CURRENT`, …)
  are repointed by `scripts/repoint_handoff.py`. The historical per-timestamp
  handoff files (thousands) are committed clutter. Propose (do not silently
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
| Convention robustness only | `SEED=42 python3 verify_convention_robustness.py` |
| Recover after interrupted run | `SEED=42 python3 run_all_verification.py --restore-only` |

- **Seed**: always `SEED=42`.
- **Data**: cached parquet in `data/` (gitignored except pinned vintages);
  cache coverage is enforced by `scripts/check_data_coverage.py`.
- **Constraints**: never re-pin goldens/data as a side effect of a run; never
  commit verification output; never claim a golden mismatch is fixed by
  re-pinning.