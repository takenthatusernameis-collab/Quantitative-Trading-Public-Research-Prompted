# Initial Task Message — Next Agentic Work Session

**Timestamp**: 2026-11-22T23:36:47Z
**Repo HEAD**: `30735ee5820e03c2e92f53ec3b9955304993c2df` (main)
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## Read this first — do NOT make another handoff-only refresh your deliverable

The research phase is **complete** (E001–E043; surviving strategies in
`ledger/RESEARCH_LEDGER.md`). The ledger shows a runaway loop (E652–E713, plus
this refresh) in which session after session did nothing except leave a new
handoff file and append a "Durable handoff refresh" ledger entry. **That loop is
the problem, not the task.**

Scale of the churn as of this writing: **8,135 git-tracked handoff files** and
514 generic alias symlinks across the mirror dirs (`handoff/`, `HANDOFFS/`,
`.handoff/`, `.kilo/`, `.kilo/handoff/`). The repo is drowning in them.

**Your job is real work, not another handoff.** If you finish having only added
a handoff file and a ledger refresh entry, you have failed. This handoff exists
because the user explicitly requested a timestamped initial-task message; that is
a one-time instruction, not a standing mandate to repeat it forever.

---

## Verified state at the moment this file was written (2026-11-22T23:36:47Z)

- `git rev-parse HEAD` -> `30735ee5820e03c2e92f53ec3b9955304993c2df` (main).
- `git status --short` -> only `__pycache__/*.pyc` noise (no tracked source
  change); `git diff HEAD -- experiments/` -> **empty**.
- `.verify_snapshot/` and `.verify_reports/` -> **absent** (no interrupted run).
- Both pure-Python golden guards executed and **PASS** on this HEAD:
  - `scripts/check_goldens_clean.py` -> `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD` (exit 0)
  - `scripts/check_golden_baseline.py` -> `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT` (exit 0)
- **Dependencies are NOT provisioned** this session (`import numpy` fails), so
  the full verification suite cannot run until you install them.

---

## Initial task (do these in order)

1. **Provision dependencies and run the fast gate.**
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
   (or `git checkout <pinned-commit> -- experiments/<file>`). Never commit
   verification output, and never "fix" a mismatch by re-pinning a golden.

3. **Address the one real open technical item (ledger E049): E041/E042
   ill-conditioned-QP drift.** The tangency QP in `src/portfolio_opt.py` still
   moves `min_var` answers by ~1e-05 under a 1-ulp input perturbation, so the
   E041 (133 numeric diffs) and E042 grid artifacts still exceed the 1e-4
   comparison tolerance and show up as drifting in the `--extended` report.
   - Do **not** silence this by re-pinning the golden (the ledger's standing
     disposition: the committed golden is authoritative, not the latest re-run).
   - The E049 rule — validate the solver answer on the problem's constraints,
     never on the solver exit status — is guarded by `tests/test_portfolio_opt.py`.
     Any fix must keep that test green.
   - A legitimate improvement is conditioning/regularization of the QP or a
     deterministic tie-break, with the effect on E041's 133 diffs and E042's grid
     quantified and recorded honestly in the ledger.

4. **Do not add a new research experiment casually.** Any new experiment must
   follow the pre-registration protocol (gates, falsification expectations,
   sensitivity grid) before it is run, per `AGENTS.md` and `ledger/PRIORITIZATION.md`.

---

## If you genuinely have nothing to do

Do **not** fabricate work and do **not** refresh the handoff. Instead, do one
concrete cleanup that reduces the churn this repo is drowning in: the historical
per-timestamp handoff files (**8,135 tracked**) are committed clutter. Propose
(do not silently execute) a `.gitignore` + `git rm --cached` plan for the
historical `handoff_*` / `HANDOFF-*` / `HANDOFF_*` files, keeping only a single
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
  commit verification output; never claim a golden mismatch is fixed by re-pinning.

---
*Timestamped initial-task handoff for the next agentic work session.*