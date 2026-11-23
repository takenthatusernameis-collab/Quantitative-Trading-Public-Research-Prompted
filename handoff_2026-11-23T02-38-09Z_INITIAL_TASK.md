# Initial Task Message — Next Agentic Work Session

**Timestamp**: 2026-11-23T02:38:09Z
**Repo HEAD**: `ca3d319217805bea2e4e5f37621d5ad049fef590` (main)
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## Initial task (do real work — do NOT make another handoff-only refresh your deliverable)

The research phase (E001–E043) is complete and the golden artifacts are verified and green. This repo is drowning in ~8,135 tracked handoff files; **break that loop by doing substantive work.**

1. **Provision dependencies and run the fast gate.**
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
   recover with `SEED=42 python3 run_all_verification.py --restore-only`. Never
   commit verification output, and never re-pin a golden to silence drift.

3. **Address the open E049 item: E041/E042 ill-conditioned-QP drift.**
   `src/portfolio_opt.py` still moves `min_var` answers by ~1e-05 under a 1-ulp
   input perturbation, so E041 (133 numeric diffs) and E042's grid exceed the
   1e-4 tolerance in `--extended`. Do **not** re-pin goldens to hide it; the
   constraint-based validation rule is guarded by `tests/test_portfolio_opt.py`
   and must stay green. Condition/regularize the QP or add a deterministic
   tie-break, quantify the effect on E041/E042 diffs honestly, and record it in
   `ledger/RESEARCH_LEDGER.md`.

4. **Do not add a new research experiment casually.** Any new experiment must
   follow the pre-registration protocol (gates, falsification expectations,
   sensitivity grid) per `AGENTS.md` and `ledger/PRIORITIZATION.md`.

---

## Verified state at handoff time (2026-11-23T02:38:09Z)

- `git rev-parse HEAD` -> `ca3d319217805bea2e4e5f37621d5ad049fef590` (main).
- `git status --short` -> only `__pycache__/*.pyc` noise; `git diff HEAD -- experiments/` -> **empty**.
- `.verify_snapshot/` and `.verify_reports/` -> **absent** (no interrupted run).
- Guards `check_goldens_clean.py` and `check_golden_baseline.py` PASS on HEAD
  (107 pinned golden artifacts match the baseline fingerprint).
- Dependencies are NOT provisioned this session (`import numpy` fails), so the
  full verification suite cannot run until you install them.

---

## Reference: key commands

| Purpose | Command |
|---|---|
| Fast gate (seconds, offline) | `SEED=42 bash scripts/check.sh` |
| Quick verification (~8 min) | `SEED=42 python3 run_all_verification.py` |
| Extended (~21 min) | `SEED=42 python3 run_all_verification.py --extended` |
| Full (~15 min) | `SEED=42 python3 run_all_verification.py --full` |
| Recover interrupted run | `SEED=42 python3 run_all_verification.py --restore-only` |
| Compile changed files | `python3 -m py_compile <file>` |

*Seed: always `SEED=42`. Never re-pin goldens/data as a side effect of a run.*

---
*Timestamped initial-task handoff for the next agentic work session.*
