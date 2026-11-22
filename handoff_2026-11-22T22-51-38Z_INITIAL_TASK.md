# Initial Task Message — Next Agentic Work Session

**Timestamp**: 2026-11-22T22:51:38Z
**Repo HEAD**: `f8a866358d64f77dd3ff890e9e617014f8b5a78b`
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## Read this first — do NOT do another handoff-only refresh

This repository's research phase is **complete** (E001–E043; survivors in
`ledger/RESEARCH_LEDGER.md`). Sessions E652–E713+ have each done nothing except
leave a new handoff and append a "Durable handoff refresh" ledger entry. That
loop is the problem, not the task. **Your job is real work, not another
handoff.** If you finish this session having only added a handoff file, you have
failed.

Do NOT append an "ENNN — Durable handoff refresh" entry to the ledger as your
deliverable. The repo already tracks thousands of handoff files; adding one
more is negative value. If you have nothing real to do, say so and stop — do not
fabricate a handoff refresh.

---

## Verified state at the moment this file was written (22:51:38Z)

- `git status` clean (aside from `scripts/__pycache__/*.pyc`).
- `main == origin/main` (HEAD `f8a866358d64f77dd3ff890e9e617014f8b5a78b`).
- Research phase complete (E001–E043). Surviving validated strategies documented
  in `ledger/RESEARCH_LEDGER.md`.
- The full prior handoff with detailed initial task is at
  `handoff_2026-11-22T22-49-06Z_INITIAL_TASK.md` — read it for the full
  task list, commands, and open technical item (ledger E049: E041/E042
  ill-conditioned-QP drift in `src/portfolio_opt.py`).

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
   Recover interrupted runs with `--restore-only`. Never commit verification output.

3. **Address the one real open technical item (ledger E049): E041/E042
   ill-conditioned-QP drift.** The tangency QP in `src/portfolio_opt.py` still
   moves `min_var` answers by ~1e-05 under a 1-ulp input perturbation.
   - Do NOT silence by re-pinning the golden.
   - Keep `tests/test_portfolio_opt.py` green (validate on constraints, not exit status).
   - Legitimate improvement: conditioning/regularization or deterministic tie-break,
     with effect on E041's 133 diffs and E042's grid quantified honestly.

4. **Do not add a new research experiment casually.** Follow pre-registration
   protocol per `AGENTS.md` and `ledger/PRIORITIZATION.md`.

---

## If you genuinely have nothing to do

Do not fabricate work and do not refresh the handoff. Instead, do one concrete
cleanup that reduces churn: propose (do not silently execute) a `.gitignore` +
`git rm --cached` plan for historical `handoff_*` / `HANDOFF-*` / `HANDOFF_*`
files, keeping only a single `HANDOFF.md` and the `ledger/`.

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
  cache coverage enforced by `scripts/check_data_coverage.py`.
- **Constraints**: never re-pin goldens/data as a side effect of a run; never
  commit verification output; never claim a golden mismatch is fixed by
  re-pinning.

(End of file)
