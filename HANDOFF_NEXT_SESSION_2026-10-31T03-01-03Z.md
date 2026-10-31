# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-31T03:01:04Z
**Branch:** `main` (up to date with origin/main)
**HEAD:** `85c8f7f` ("chore(kilo): checkpoint agent session")
**Working tree:** clean of source/data changes
**Verification snapshot:** none active (`.verify_snapshot/` absent)

---

## INITIAL TASK (do first)

**Confirm baseline integrity before making any changes or running verification.**

1. **Run baseline integrity checks**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match, data coverage, portfolio_opt tests, convention robustness, template validation, experiment-script imports.

2. **If checks fail, remediate before proceeding**
   - **Goldens differ from HEAD** → Restore from the commit whose SHA-256 matches `ledger/golden_baseline.json` (or `SEED=42 python3 run_all_verification.py --restore-only`, or `git checkout -- experiments/`).
   - **Active verification snapshot** → If `.verify_snapshot/ACTIVE.json` exists, recover with `--restore-only` before proceeding.
   - **Pinned baseline mismatch** → Investigate with `python3 scripts/check_golden_baseline.py`. **Never re-pin to silence drift** — re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff with explicit justification.
   - **Cache coverage failure** → Ensure pinned data in `ledger/data_baseline.json` exists and is git-tracked. To add inputs, commit files and re-pin with `python3 scripts/check_data_coverage.py --update`.

3. **After confirming green checks, idle awaiting explicit user direction**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin baselines without explicit instruction and justification in the diff.
   - Do **NOT** run extended/full verification suites without explicit instruction.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Goldens:** `experiments/*.json` match HEAD. `ledger/golden_baseline.json` pins tracked artifacts (107 pinned, all match). `ledger/data_baseline.json` enforces cache coverage.
- **Open items:** See `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` (optimizer determinism E049; E041/E030 drift; cache coverage E048; CI gate workflow needs maintainer).
- **Environment:** Python 3 research repo. Dependencies per `requirements.txt`. `cvxpy`/`cvxopt` optional (falls back to scipy).

---

## Key commands

```bash
# Baseline integrity (required first)
SEED=42 bash scripts/check.sh

# Quick/full verification (only if explicitly requested)
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended  # extended (~21 min)
SEED=42 python3 run_all_verification.py --full      # full (~15 min)

# Recovery
SEED=42 python3 run_all_verification.py --restore-only

# Guards
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
python3 scripts/check_goldens_clean.py
```
