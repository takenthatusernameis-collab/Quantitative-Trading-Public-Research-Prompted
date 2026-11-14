# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC): 2026-11-14T22:24:03Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `5e22bf17` ("chore(kilo): checkpoint agent session"); `origin/main...HEAD` = `0 0` (in sync)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- **Working tree:** clean of source/data changes. `git status --short | grep -v __pycache__` is empty; only tracked `__pycache__/*.pyc` build artifacts differ (gitignored build output — do not commit).
- **Verification snapshot:** none active (`.verify_snapshot/` and `.verify_reports/` absent). No interrupted verification run.
- **Goldens:** `experiments/*.json` match HEAD. Guard suite re-run this session (SEED=42):
  - `SEED=42 bash scripts/check.sh` → **exit 0**, "=== All checks passed ===" (py_compile, JSON artifacts parse, goldens clean vs HEAD, pinned golden baseline, data coverage, `test_portfolio_opt`, convention robustness, template validation, experiment imports).
  - `scripts/check_json_artifacts.py` → ALL COMMITTED JSON ARTIFACTS PARSE OK
  - `scripts/check_goldens_clean.py` → ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD
  - `scripts/check_golden_baseline.py` → ALL PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT
  - `scripts/check_data_coverage.py` → ALL PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED
- **Environment (important):** Python 3.12.3 with dependencies from `requirements.txt` installed (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). If the environment is reset, re-run `pip3 install --break-system-packages -r requirements.txt` before trusting `check.sh` (otherwise a `ModuleNotFoundError` can be mistaken for a baseline failure).
- **Research phase complete:** E001–E051; surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Durable-handoff refreshes recorded through E339.

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

This session wrote this durable handoff after confirming baseline integrity (`check.sh` exit 0). Before making any changes or running verification:

1. **Confirm repo state**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0. If it fails with `ModuleNotFoundError`, install dependencies (`pip3 install --break-system-packages -r requirements.txt`) and re-run — do not treat a dependency error as a baseline failure.

2. **If checks fail for a real reason**
   - **Goldens differ from HEAD** → restore with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`), or from the commit whose SHA-256 matches `ledger/golden_baseline.json`.
   - **Active verification snapshot** → if `.verify_snapshot/ACTIVE.json` exists, recover with `--restore-only` before proceeding.

3. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin baselines without explicit instruction and justification in the diff.
   - Do **NOT** commit `__pycache__/*.pyc` noise.

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

- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver answers on constraints, never solver exit status. The tangency QP is ill-conditioned — 1-ulp input changes move `min_var` by ~1e-05; E041/E042 grid artifacts may drift 29–133 differences. **Do not re-pin to silence.**
- **E041 drift:** 133 numeric differences (1-ulp QP sensitivity); the 3 structural differences are already fixed. Open item in ledger; do not re-pin.
- **CI gate:** `.github/workflows/verification-gate.yml` requires a maintainer via the GitHub UI; template at `.github/workflow-templates/verification-gate.yml`.
- **Always use `SEED=42`.** Never commit verification output.

---

## Durable artifact

Primary: repo root `handoff_2026-11-14T22-24-03Z_INITIAL_TASK.md`.
Mirrors: `handoff/`, `HANDOFFS/`, `.handoff/` (both `handoff_`-prefixed and bare-timestamp names), `.kilo/`, and `.kilo/handoff/`.
Generic canonical pointers repointed with `python3 scripts/repoint_handoff.py handoff_2026-11-14T22-24-03Z_INITIAL_TASK.md`.

Supersedes the previous INITIAL_TASK handoff (`handoff_2026-11-14T22-21-36Z_INITIAL_TASK.md`, ledger E339, HEAD `0c7f8041`). Written by the agent at 2026-11-14T22:24:03Z.