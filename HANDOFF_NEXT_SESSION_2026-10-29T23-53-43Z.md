# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-29T23:53:43Z (message time)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `3cb93c6` (chore(kilo): checkpoint agent session, 2026-10-29 23:53:34 UTC). Up to date with `origin/main`.

## Baseline state — VERIFIED THIS SESSION (do not assume; re-verify)

- `SEED=42 bash scripts/check.sh` → **exit 0, "=== All checks passed ==="**. All committed golden artifacts match HEAD; all 107 pinned golden artifacts match the `ledger/golden_baseline.json` fingerprint; all experiment-script imports OK; E042 lead re-verified PARTIAL 4/5 as recorded.
- Working tree: **clean of tracked changes**. Only `__pycache__/*.pyc` modified (gitignored — ignore them).
- No `.verify_snapshot/` directory, no `ACTIVE.json` → **no interrupted verification run to recover**.
- The `FAIL` lines in `check.sh` output are **intentional negative-test fixtures**, not real failures:
  - `check_json_artifacts.py:238` feeds `experiments/d.json`/`badlist.json`/`b.json`/`x.json`/`e2.json`/`u.json` and asserts they are rejected.
  - `check_goldens_clean.py` asserts a stale snapshot owned by pid 999999 is reported.
  - `check_data_coverage.py` asserts a missing manifest (`nope.json`) and untracked/unpinned data files are reported.
  - These files do **not** exist in the working tree and are not git-tracked. The suite's final line is the pass marker.

## Initial Task (Start Here)

Verify the baseline is clean before any work.

1. Run `SEED=42 bash scripts/check.sh` — must exit 0 with "=== All checks passed ===". Treat the negative-test FAIL lines above as expected.
2. Run `git status --short` / `git diff --name-only` — confirm clean tree (only `__pycache__/*.pyc`, gitignored).
3. If an interrupted verification left dirty `experiments/*.json`, restore:
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).

Do not re-pin goldens to silence drift. Keep committed goldens authoritative.
Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` first.

## Known Open Items (Do Not "Fix" By Re-Pinning)

- **E041 numeric drift (open):** ~133 numeric differences remain (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism gating fixed per ledger E049). Do **not** re-pin `experiments/e041_*.json`.
- **E042 grid artifacts:** 1-ulp sensitivity can appear; do not re-pin goldens.
- **E030:** numeric diffs on near-zero quantities (documented). Do not re-pin.
- **Data coverage:** Inputs must remain tracked and pinned in `ledger/data_baseline.json`. Never re-pin as a side-effect of verification.
- **Pinned fundamentals/vintages:** `data/fundamentals/` (per `data/fundamentals_vintages.json`) and `data/vintages.json` are part of reproducibility. Treat as canonical.

## Precise Task (bounded, optional)

Re-run the verification suite to confirm stability:

```bash
SEED=42 python3 run_all_verification.py --extended
```

Expect the pre-existing E030/E041 drift above. Do **not** weaken tolerances, skip drivers, or modify committed goldens. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

## Quick Commands

```bash
# Fast gate
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Recover after interruption
SEED=42 python3 run_all_verification.py --restore-only
```

## Notes for the next session

- The `exact_qp()` active-set KKT solver is wired into `src/portfolio_opt.py` at the `max_sharpe` tangency branch (`:435`), and the `min_var`/`risk_parity` branches (`:386`, `:401`). The SLSQP helper `solve_qp` at `:344` is **dead code** (defined, never called — grep confirms no call sites). Deleting it is a no-op cleanup; flagged rather than removed.
- The prior handoff's stated HEAD (`8e2af23`) is stale; this handoff records `3cb93c6`, which differs from `8e2af23` **only** in handoff/markdown files (symlinks `handoff.md` → this file, `handoff_next.md` → the 23:50 handoff). No source, experiment, or data files changed between them.