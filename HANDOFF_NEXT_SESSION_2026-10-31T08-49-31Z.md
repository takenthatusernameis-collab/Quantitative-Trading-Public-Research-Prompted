# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-31T08:49:31Z
**Branch:** main
**HEAD:** 0b2e0d4
**Working tree:** clean of tracked changes (no modifications pending).
**Verification snapshot:** none active (`.verify_snapshot/` absent, no `ACTIVE.json`). No run in progress; nothing to recover.
**Session context:** Durable handoff created per request. Repository in verified stable state.

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

Before making any changes or running verification:

1. **Confirm repo state**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0. Runs convention robustness, template validation, goldens guards (`check_goldens_clean.py`, `check_golden_baseline.py`), data coverage (`check_data_coverage.py`), `tests/test_portfolio_opt.py`, and experiment-script imports.

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

- **Research phase complete:** E001–E043. Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baseline integrity enforced:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py` are first-class steps in `scripts/check.sh` and the verification suite.
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver answers on constraints, not exit status. `tests/test_portfolio_opt.py` pinned.
- **No open task.** Await explicit user direction.
