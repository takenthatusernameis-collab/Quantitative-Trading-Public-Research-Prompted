# HANDOFF: Next Agentic Work Session

**Timestamp (UTC):** 2026-10-31T10:54:33Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Git repo:** yes
**Branch:** main
**HEAD:** fa2faf1 chore(kilo): checkpoint agent session

---

## Clear Initial Task (for next session)

**Goal:** Confirm baseline integrity and a clean, reproducible repo state before making any changes.

**Steps (in order):**

1. Check git state:
   ```bash
   git status --short
   git log -1 --oneline
   ```
   Expected: only the 12 stale `__pycache__/*.pyc` modifications. If any source or `experiments/*.json` differs from HEAD, stop and report.

2. Run fast integrity checks (offline, no golden writes):
   ```bash
   SEED=42 bash scripts/check.sh
   ```

3. If `check.sh` passes, run quick verification (restores goldens):
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   (~8 min). Do not interrupt.

4. Report outcome; recover interrupted runs with `SEED=42 python3 run_all_verification.py --restore-only`.

**Known open context:**
- E041/E042 sensitivity grids and the full E042 confirmatory golden are not byte-reproducible in this sandbox (SLSQP optimizer float drift; see `HANDOFF_REPRO_CAVEAT.md`). No gate or decision is affected.
- CI workflow `.github/workflows/verification-gate.yml` still requires maintainer creation via GitHub UI; template at `.github/workflow-templates/verification-gate.yml`.

**Constraints:**
- Always use `SEED=42`.
- Never leave verification half-finished; do not commit verification output.
- Do not modify committed goldens, weaken tolerances, skip drivers, or change gate logic.
- Do not change validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).

---

## Handoff Metadata

- **Created by:** Kilo (agentic session)
- **Reason:** Durable handoff for next agentic work session; timestamped initial task message per request.
- **Next action:** Execute the initial task above.

(End of file)
