# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC): 2026-11-14T15-38-33Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 188ac90c (up to date with origin/main)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- **Working tree:** clean of source/data changes (only `__pycache__/*.pyc` build artifacts, gitignored, not source). `git status --short | grep -v __pycache__` empty.
- **Verification snapshot:** none active (`.verify_snapshot/` absent).
- **Goldens:** `experiments/*.json` match HEAD. `ledger/golden_baseline.json` pins tracked artifacts; `ledger/data_baseline.json` enforces cache coverage.
- **Environment:** Python 3.12.3, deps from `requirements.txt` installed (numpy/pandas/scipy/pyarrow/statsmodels/yfinance). If reset: `pip3 install --break-system-packages -r requirements.txt`.
- **Research phase complete:** E001–E051; surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

This session performed no technical work — it only wrote this durable handoff. Before making any changes or running verification:

1. **Confirm repo state**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match, data coverage, portfolio_opt tests, convention robustness, template validation, experiment-script imports.

2. **If checks fail**
   - **Goldens differ from HEAD** → restore with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`), or from the commit whose SHA-256 matches `ledger/golden_baseline.json`.
   - **Active verification snapshot** → if `.verify_snapshot/ACTIVE.json` exists, recover with `--restore-only` before proceeding.

3. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin baselines without explicit instruction and justification in the diff.

---

## Key Commands

```bash
# Baseline integrity (required first)
SEED=42 bash scripts/check.sh

# Quick / extended / full verification
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # (~21 min)
SEED=42 python3 run_all_verification.py --full       # (~15 min)

# Recovery / guards
SEED=42 python3 run_all_verification.py --restore-only
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
python3 scripts/check_goldens_clean.py
```

---

## Known Open Items (read AGENTS.md before acting)

- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver answers on constraints, never solver exit status. Tangency QP ill-conditioned — 1-ulp input changes move `min_var` by ~1e-05; E041/E042 grid artifacts may drift 29–133 differences. **Do not re-pin to silence.**
- **CI gate:** `.github/workflows/verification-gate.yml` requires maintainer via GitHub UI; template at `.github/workflow-templates/verification-gate.yml`.
- Always use `SEED=42`. Never commit verification output.

---

## Durable artifact

Primary: `.handoff/2026-11-14T15-38-33Z_INITIAL_TASK.md`. Mirror: repo root `handoff_2026-11-14T15-38-33Z_INITIAL_TASK.md`.

Supersedes previous INITIAL_TASK handoffs. Written by agent at 2026-11-14T15:38:33Z.
