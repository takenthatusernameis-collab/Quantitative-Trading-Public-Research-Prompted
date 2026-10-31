# HANDOFF: Next Agentic Work Session

**Timestamp (UTC):** 2026-10-31T09:57:22Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Git repo:** yes
**Branch:** main
**HEAD:** 38cdc66 chore(kilo): checkpoint agent session
**Working tree:** Only 12 tracked `__pycache__/*.pyc` modifications (stale bytecode). No source, golden, or data changes.
**Verification snapshot:** none active (`.verify_snapshot/` absent). Nothing to recover.

---

## Current State

- **Research phase:** Complete (E001–E049). Surviving strategies in `ledger/RESEARCH_LEDGER.md` (tail at E049).
- **Goldens:** `experiments/*.json` are canonical. Verification backs up/restores them — never leave a run half-finished.
- **Integrity guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- **Data:** Pinned vintages in `data/vintages.json` (2026-10-12), `data/` has committed 2026-10-11, fundamentals pinned in `data/fundamentals/` (E029 offline-reproducible). Runs use `QUANT_RESEARCH_OFFLINE=1`.
- **Known drift (reporting-only):** E041 ~133 numeric diffs (ill-conditioned QP), E030 near-zero numeric diffs (input pinned). Do **not** re-pin goldens.

---

## INITIAL TASK FOR NEXT AGENT (Start Here)

**Objective:** Verify baseline integrity and confirm the repo is clean/reproducible before any changes.

### Step 1: Git state (30s)
```bash
git status --short
git log -1 --oneline
```
**Pass:** only `__pycache__/*.pyc` modified. If any source or `experiments/*.json` differs from HEAD → **STOP and report**.

### Step 2: Fast integrity checks (1-2 min)
```bash
SEED=42 bash scripts/check.sh
```
Runs py_compile, convention checks, golden/baseline/data guards, unit tests, convention robustness, template validation, experiment imports.

### Step 3: Quick verification (restores goldens, ~8 min)
```bash
SEED=42 python3 run_all_verification.py
```
Re-runs the 8-driver quick block and validates. Goldens backed up/restored automatically. **Do not interrupt.**

### Step 4: Report
Return a concise report with:
- Git state (branch/HEAD + diff summary)
- `check.sh` result (pass/fail + first failing check if any)
- `run_all_verification.py` summary (pass/fail, any drivers flagged)
- Confirmation `experiments/*.json` unchanged vs HEAD/baseline
- If recovery needed: use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` as appropriate

---

## Hard Rules
- Always use `SEED=42`
- Never leave verification half-finished
- Never re-pin goldens, weaken tolerances, skip drivers, or change gates
- Never modify validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`)
- Leave `__pycache__/*.pyc` alone
- Do not commit verification output

## Key Files
- `AGENTS.md` — commands/conventions/integrity
- `ledger/RESEARCH_LEDGER.md` — history (E001–E049)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `run_all_verification.py`, `scripts/check.sh`
- `HANDOFF_REPRO_CAVEAT.md`

**Handoff created by:** Kilo
**Reason:** Durable timestamped initial task for next agentic session.
