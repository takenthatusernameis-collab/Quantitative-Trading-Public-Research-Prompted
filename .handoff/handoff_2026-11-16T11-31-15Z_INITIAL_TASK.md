# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T11:31:15Z
**Workspace:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD context:** inspect with `git status --short` and `git log -1 --oneline` before changes.

---

## Initial task (do first)

1. **Confirm repo baseline integrity**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match, data coverage, portfolio_opt tests, convention robustness, template validation, experiment-script imports.

2. **If checks fail**
   - **Goldens differ from HEAD / stale `.verify_snapshot/ACTIVE.json`** → recover: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` (or restore the pinned commit per `AGENTS.md`).
   - **Never re-pin to silence drift** — re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff.

3. **Then await explicit user direction**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin baselines without explicit instruction and justification in the diff.

---

## Project state

- Research phase complete (E001–E043). Validated strategies and dispositions: `ledger/RESEARCH_LEDGER.md`.
- Canonical experiment artifacts: `experiments/*.json`; goldens pinned in `ledger/golden_baseline.json`; data coverage pinned in `ledger/data_baseline.json`.
- Only expected working-tree churn: `__pycache__/*.pyc` build artifacts (gitignored).
- Known open item (read `AGENTS.md` before acting): optimizer/QP 1-ulp numeric sensitivity — E041/E042 grid artifacts may drift in extended checks. **Do not re-pin to silence this** (see ledger E049).
- CI workflow still requires maintainer action via GitHub UI; template at `.github/workflow-templates/verification-gate.yml`.

---

## Key commands

```bash
SEED=42 bash scripts/check.sh                        # convention + integrity (~seconds)
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # (~21 min)
SEED=42 python3 run_all_verification.py --restore-only # recover interrupted run
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
```

---

**Durable artifact:** mirrored at `.handoff/handoff_2026-11-16T11-31-15Z_INITIAL_TASK.md` and `handoff_2026-11-16T11-31-15Z_INITIAL_TASK.md` (repo root). Pointers (`current`, `CURRENT`, `LATEST`, `handoff_current`, etc.) should reference this file.

**Ready to start at step 1.**
