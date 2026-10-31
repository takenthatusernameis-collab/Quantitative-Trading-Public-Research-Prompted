# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-10-31T06:08:20Z
**Branch:** `main`
**HEAD:** `d8fac1c` (chore(kilo): checkpoint agent session)
**Working tree:** clean of tracked changes — only `__pycache__/*.pyc` artifacts (gitignored; ignore them).
**Verification snapshot:** none active (`.verify_snapshot/` absent, no `ACTIVE.json`). No run in progress; nothing to recover.

---

## INITIAL TASK (do first)

**Repository is fully verified and stable. No new research is warranted. Your primary task is to confirm stability, not to change anything.**

1. Run the fast baseline integrity check:
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0. This runs `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `test_portfolio_opt.py`, template validation, and experiment-script imports.
2. `check_goldens_clean.py` compares the working tree to HEAD. Since HEAD is a checkpoint commit, restored goldens may differ from HEAD — that is expected; the pinned baseline in `ledger/golden_baseline.json` is authoritative. Do **not** run `git checkout -- experiments/`.
3. If any pinned artifact differs from its SHA-256 in `ledger/golden_baseline.json`, restore from the matching commit (`git checkout <commit> -- experiments/<file>`); never re-pin without explicit justification.
4. After green checks, idle awaiting explicit user direction. Do not modify goldens, re-pin baselines, or run extended/full verification without explicit instruction.

---

## Current state

- Research phase complete (E001–E049). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- All guards in place and passing: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `tests/test_portfolio_opt.py`, `verify_convention_robustness.py`, template validation, experiment-script imports.
- Manifests untouched (`ledger/golden_baseline.json`, `ledger/data_baseline.json`). No source or data changes.
- Reproducibility caveat documented: E041/E042 sensitivity grids are not byte-reproducible in this sandbox (SLSQP/BLAS-sensitive); no gate or decision affected. See `HANDOFF_REPRO_CAVEAT.md`.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json` via `.verify_snapshot/`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).

(End of handoff)
