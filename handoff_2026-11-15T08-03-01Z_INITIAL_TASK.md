# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T08:03:01Z
**Session**: Initial handoff for next agentic work session
**Workspace**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 drivers in the 5a block)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 committed drivers)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Important Notes

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG).
- **Golden files**: `experiments/*.json` are committed artifacts — never commit verification output.
- **Recovery**: If verification is interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage enforced via `scripts/check_data_coverage.py`. Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`); missing pinned caches fail hard.
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).
- **Optimizer determinism**: `src/portfolio_opt.py` validates solver answers on constraints, never exit status. Do **not** re-pin E041/E042 grid goldens to silence numeric drift.
- **CI workflow**: Cannot be created by agents. Template at `.github/workflow-templates/verification-gate.yml`; instructions in `VERIFICATION_GATE_TEMPLATE.md`.

## Current State

- Research phase complete (E001–E043); ledger documents surviving validated strategies.
- Verification suite validates reproducibility across experiment drivers.
- Working tree state captured at snapshot time — verify `git status --short` before acting.

## Initial Task for the Next Session

**Primary objective:** Verify repository integrity and establish a clean baseline before making any changes.

### Concrete steps (in order)

1. **Check git state**
   ```bash
   git status --short
   ```
   Ensure no unexpected modifications to `experiments/`, `ledger/`, or `data/`. If `experiments/` differ from HEAD, restore first.

2. **Run fast integrity check**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Catches convention, template, py_compile, golden, and data coverage issues quickly.

3. **Run quick verification (recommended)**
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

4. **Review results**
   - If all checks pass: repo is clean and reproducible. Await the user's next requested change.
   - If failures occur: follow `AGENTS.md` guardrails. Do **not** re-pin goldens/data as a side effect of verification.

## Key Pointers

- **Ledger:** `ledger/RESEARCH_LEDGER.md`
- **Golden pin:** `ledger/golden_baseline.json`
- **Data pin:** `ledger/data_baseline.json`
- **Verification:** `run_all_verification.py`, `scripts/check.sh`, `make verify-quick/extended/full`
- **Conventions:** `AGENTS.md`
- **Project config:** `kilo.json`

**Ready to start at step 1.**