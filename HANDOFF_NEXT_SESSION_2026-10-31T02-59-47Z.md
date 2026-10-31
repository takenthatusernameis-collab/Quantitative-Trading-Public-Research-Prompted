# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-31T02-59-47Z (UTC)
**Branch:** `main` (up to date with origin/main)
**HEAD:** `b7b5e15` ("chore(kilo): checkpoint agent session")
**Working tree:** clean of source/data changes.
**Verification snapshot:** none active (`.verify_snapshot/` absent).

---

## INITIAL TASK (do first)

No technical task has been assigned yet. This session only wrote this handoff.

Before making any changes or running verification:

1. **Confirm baseline integrity**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match, data coverage, portfolio_opt tests, convention robustness, template validation, experiment-script imports.

2. **If checks fail**
   - **Goldens differ from HEAD** → restore from the commit whose SHA-256 matches `ledger/golden_baseline.json` (or `SEED=42 python3 run_all_verification.py --restore-only`, or `git checkout -- experiments/`).
   - **Never re-pin to silence drift** — re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff with justification.
   - **Active verification snapshot** → if `.verify_snapshot/ACTIVE.json` exists, recover with `--restore-only` before proceeding.
   - **Cache coverage failure** → ensure pinned data in `ledger/data_baseline.json` exists and is git-tracked. To add inputs, commit files and re-pin with `python3 scripts/check_data_coverage.py --update`.

3. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin baselines without explicit instruction and justification in the diff.
   - Do **NOT** run extended/full verification suites without explicit instruction.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Working tree:** `git status --short | grep -v __pycache__` shows no changes.
- **Verification state:** No active verification snapshot in `.verify_snapshot/`.
- **Goldens:** `experiments/*.json` match HEAD. `ledger/golden_baseline.json` pins tracked artifacts (107 pinned, all match). `ledger/data_baseline.json` enforces cache coverage.
- **Open items:** see `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` (optimizer determinism E049; E041/E030 drift; cache coverage E048; CI gate workflow needs maintainer).

---

## Key commands

```bash
# Baseline integrity (required first)
SEED=42 bash scripts/check.sh

# Quick/full verification (only if explicitly requested)
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
