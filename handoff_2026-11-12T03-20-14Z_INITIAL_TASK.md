# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-12T03:20:14Z (UTC)
**Branch:** `main` (up to date with origin/main)
**HEAD:** `0d366136` chore(kilo): checkpoint agent session
**Working tree:** clean of source/data changes (`__pycache__/*.pyc` modifications present as build artifacts; no tracked source changes)
**Verification snapshot:** none active (`.verify_snapshot/` absent)

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

This session performed no research, code, or data changes — it only wrote this handoff. Before making any changes or running verification:

1. **Confirm repo state**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match (`ledger/golden_baseline.json`), data coverage (`ledger/data_baseline.json`), portfolio_opt tests, convention robustness, template validation, experiment-script imports.

2. **If checks fail**
   - **Goldens differ from HEAD** → restore from the commit whose SHA-256 matches `ledger/golden_baseline.json` (preferred), or `SEED=42 python3 run_all_verification.py --restore-only`, or `git checkout -- experiments/` (only if HEAD is known-good).
   - **Never re-pin to silence drift** — re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff with justification.
   - **Active verification snapshot** → if `.verify_snapshot/ACTIVE.json` exists, recover with `--restore-only` before proceeding.

3. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin `ledger/golden_baseline.json` / `ledger/data_baseline.json` without explicit instruction.

---

## Current state

- **Research phase complete:** E001–E043. Findings and dispositions are in `ledger/RESEARCH_LEDGER.md`.
- **Goldens/baselines:** `experiments/*.json` are canonical artifacts pinned in `ledger/golden_baseline.json`; data inputs pinned in `ledger/data_baseline.json`.
- **Verification suite:** `run_all_verification.py` backs up/restores goldens; must not be left half-finished. Use `--restore-only` to recover.
- **Key constraints (read `AGENTS.md`):**
  - `SEED=42` for reproducibility.
  - Cache coverage enforced (E048): drivers run with `QUANT_RESEARCH_OFFLINE=1` during verification; missing pinned cache entries fail hard.
  - Optimizer determinism (E049): tangency QP ill-conditioning means E041/E042 grid artifacts can drift numerically (1-ulp sensitivity). Do not re-pin to silence.
  - CI workflow `.github/workflows/verification-gate.yml` requires maintainer action (agents cannot push workflows); template at `.github/workflow-templates/verification-gate.yml`.

## Key commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # (~21 min)
SEED=42 python3 run_all_verification.py --full       # (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
python3 scripts/check_goldens_clean.py
```

## Environment note

- Python 3.12.3; deps in `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). If environment is reset: `pip3 install --break-system-packages -r requirements.txt`.
