# Handoff — 2026-10-28T14-20-15Z

- Repo: Quantitative-Trading-Public-Research-Prompted
- Working dir: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- Branch: main
- HEAD: a1de6fa chore(kilo): checkpoint agent session

## Current state
- Research phase complete (E001–E043). Surviving validated strategies documented in ledger/RESEARCH_LEDGER.md.
- Canonical artifacts: experiments/*.json (goldens). Do NOT modify them as a side effect of verification.
- Baseline integrity guards enforced: scripts/check_goldens_clean.py, scripts/check_golden_baseline.py, scripts/check_data_coverage.py.
- Verification suite (run_all_verification.py) backs up/restores goldens and refuses to run if a snapshot is owned/live.

## Clear initial task for next session
1. **Verify clean baseline first**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect all checks to pass (py_compile, goldens clean vs HEAD, golden baseline pin match, data coverage, portfolio_opt tests).

2. **Run quick verification (recommended)**
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   If interrupted for any reason, recover with:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```

3. **Review open items before making changes**
   - ledger/RESEARCH_LEDGER.md — note E049 (optimizer determinism / E041 drift). Do not re-pin goldens to silence numeric drift.
   - ledger/golden_baseline.json and ledger/data_baseline.json before any intentional re-pinning.

## Constraints / reminders
- Always use SEED=42.
- Never leave a verification run half-finished.
- Data: pinned vintages in data/vintages.json / data/fundamentals_vintages.json. Missing caches fail under offline verification.
- CI workflow cannot be created by agents; template at .github/workflow-templates/verification-gate.yml.
- Follow AGENTS.md conventions (pre-registration, multiple-testing discipline, negative results recorded honestly).
- If scripts/check.sh reports golden mismatch, fix before committing. Never re-pin baselines as a side effect of running verification.

## Suggested first commands
```bash
git status --short
git log -1 --oneline
SEED=42 bash scripts/check.sh
```
