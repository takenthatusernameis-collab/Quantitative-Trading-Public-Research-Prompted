# Durable Handoff — Next Agentic Work Session

**Generated:** 2026-10-30T14-29-03Z (UTC)
**Session:** handoff-only session (no technical work performed)
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `3e5d836` (HEAD; checkpoint commit)
**Previous handoff:** `HANDOFF_NEXT_SESSION_2026-10-30T14-28-09Z.md` (symlinked as `handoff.md`)

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

This session performed no technical work — it only wrote this handoff. The working tree is clean of source/data changes aside from tracked `__pycache__/*.pyc` build artifacts.

1. **Confirm repo state before anything else**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match, data coverage, portfolio_opt tests, convention robustness, template validation, experiment-script imports.

2. **If checks fail**
   - **Goldens differ from HEAD** → restore from the commit whose SHA-256 matches `ledger/golden_baseline.json` (or `SEED=42 python3 run_all_verification.py --restore-only`).
   - **Never re-pin to silence drift** — re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff.
   - **Active verification snapshot** → if `.verify_snapshot/ACTIVE.json` exists, recover with `--restore-only` before proceeding.

3. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin baselines without explicit instruction and justification in the diff.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Working tree:** `git status --short` shows only tracked `__pycache__/*` artifacts (13 .pyc files). No source/data changes.
- **Verification state:** `.verify_snapshot/` does **NOT** exist — no recovery needed.
- **Goldens:** `experiments/*.json` match HEAD. `ledger/golden_baseline.json` pins 107 tracked artifacts. `ledger/data_baseline.json` enforces cache coverage.
- **Environment:** Python 3.12.3 with deps from `requirements.txt` installed in this sandbox (numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0, yfinance 1.7.0). If reset, run `pip3 install --break-system-packages -r requirements.txt` first.

---

## Known open items (read AGENTS.md before acting)

- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver answers on the problem's constraints, never on the solver's exit status; pinned by `tests/test_portfolio_opt.py` (first-class step of `scripts/check.sh`). The tangency QP remains ill-conditioned — 1-ulp input perturbations move `min_var` answers by ~1e-05, so E041/E042 grid artifacts may drift by 29–133 differences. **Do not re-pin to silence this.** See ledger E049.
- **E041 drift (E049):** 3 structural diffs are resolved; 133 numeric diffs remain (within ill-conditioning). Open item in the ledger.
- **Cache coverage enforced (E048):** `scripts/check_data_coverage.py` validates all data inputs are pinned in `ledger/data_baseline.json`. Verification runs every driver with `QUANT_RESEARCH_OFFLINE=1`, so missing cache entries fail hard.
- **CI gate workflow:** `.github/workflows/verification-gate.yml` still requires maintainer action via GitHub UI (automated agents cannot push workflows). Copyable template at `.github/workflow-templates/verification-gate.yml`.

---

## Key commands

```bash
# Baseline integrity (required first)
SEED=42 bash scripts/check.sh

# Quick/full verification
SEED=42 python3 run_all_verification.py        # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended  # (~21 min)
SEED=42 python3 run_all_verification.py --full      # (~15 min)

# Recovery
SEED=42 python3 run_all_verification.py --restore-only

# Guards
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
python3 scripts/check_goldens_clean.py
```
