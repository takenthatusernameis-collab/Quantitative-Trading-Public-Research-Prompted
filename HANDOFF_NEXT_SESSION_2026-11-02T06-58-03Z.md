# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-02T06-58-03Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** $(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted rev-parse --short HEAD 2>&1 | tail -1)
**State:** Research phase complete (E001–E050). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Working tree clean at current HEAD (only gitignored `__pycache__/*.pyc` may differ). No live verification snapshot expected.

## Initial task message for the next agentic work session

> **START HERE:** Verify baseline integrity is clean before starting any new work. The repo has completed research phases through E050 (E049/E050 tangency-QP optimizer determinism closed). Do not re-open those items or re-pin goldens to silence drift.

**Required sequence (do in order):**

1. **Environment setup** (if fresh/reset):
   ```bash
   pip install -r requirements.txt
   ```
   Dependencies: numpy, pandas, scipy, pyarrow, statsmodels, yfinance. cvxpy/cvxopt optional.

2. **Verify baseline integrity (fast checks):**
   ```bash
   cd /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
   SEED=42 bash scripts/check.sh
   ```
   Expected: exits 0 with `=== All checks passed ===`. This runs `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, portfolio-opt tests, and template validation.

3. **Confirm clean state:**
   ```bash
   git status --short
   ```
   Only `__pycache__/*.pyc` are acceptable. Do **not** commit verification output.

4. **If interrupted run detected**, recover before proceeding:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   git status --short
   ```
   (Only if working tree shows modified tracked artifacts in `experiments/`.)

5. **Proceed with next research task:**
   - Read `ledger/RESEARCH_LEDGER.md` to identify the next unstarted/open task (beyond E050).
   - Follow pre-registration, multiple-testing discipline, and all constraints below.
   - Run `python3 -m py_compile` on changed files.
   - Never commit verification output or re-pin goldens as a side effect of running verification.

## Critical Constraints (must follow)

- **Golden integrity:** `experiments/*.json` are canonical. `run_all_verification.py` backs up/restores; never leave a verification run half-finished. Use `--restore-only` to recover.
- **Golden baseline pin:** `scripts/check_golden_baseline.py` compares against `ledger/golden_baseline.json`. Only re-pin via `python3 scripts/check_golden_baseline.py --update` if the change is intentional and explicitly requested (do **not** let verification do this).
- **Data coverage:** All `data.download()` call sites must have committed, git-tracked caches pinned in `ledger/data_baseline.json`. Missing/unpinned inputs will fail under `QUANT_RESEARCH_OFFLINE=1`.
- **Known closed:** E049/E050 (tangency-QP optimizer determinism) are closed. Do **not** re-open. E041/E042 numeric drift from ill-conditioned QP remains (1-ulp) — do **not** re-pin to silence.
- **Pinned data:** E029 fundamentals pinned in `data/fundamentals/` (offline reproducible). E030 panel committed (offline reproducible). Vintages: `data/vintages.json` (2026-10-12), committed 2026-10-11 vintage.
- **Reproducibility:** Always use `SEED=42`. Honor pinned cache vintages.
- **Discipline:** Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without strong justification and explicit pre-registration updates.
- **CI:** Workflow template at `.github/workflow-templates/verification-gate.yml`; actual workflow cannot be auto-created by agents.
- **Conventions:** Follow `AGENTS.md` (commands, conventions, baseline integrity rules).

## Quick References

- **Commands:** `make check` | `make verify` | `make verify-quick` | `make verify-extended` | `make verify-full`
- **Key files:** `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `run_all_verification.py`, `scripts/check.sh`
- **Guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only`

## Suggested First Command
```bash
cd /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted && SEED=42 bash scripts/check.sh
```
