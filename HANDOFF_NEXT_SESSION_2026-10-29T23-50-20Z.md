# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-29T23:50:20Z (message time)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `8e2af23` (working tree clean of tracked changes; only `__pycache__/*.pyc`, gitignored; no `.verify_snapshot/` active; no interrupted run to recover).

## Initial Task (Start Here)

Verify the baseline is clean before any work.

1. Run `SEED=42 bash scripts/check.sh` — all guards must pass with no golden diffs.
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

## Session Summary (what I did and found)

The recommended task in the prior handoffs was: *replace the SLSQP QP solves in `src/portfolio_opt.py` with a well-conditioned, deterministic solver (exact active-set enumeration of all KKT points for N <= 5), then deliberately re-pin affected artifacts.* That work is **already complete** in the committed tree:

- `exact_qp()` (active-set KKT enumeration) is wired into the `max_sharpe` tangency branch at `src/portfolio_opt.py:435`, and into the `min_var` / `risk_parity` branches at `src/portfolio_opt.py:386` and `:401`.
- The `solve_qp` SLSQP helper at `src/portfolio_opt.py:344` is now **dead code** — it is defined but never called anywhere in the repo (grep confirmed: only its own definition matches). It can be deleted, but that is a cleanup with no behavioral effect and no golden impact; flagging it rather than removing it.
- Pinned by `tests/test_portfolio_opt.py` (first-class step of `scripts/check.sh`), which asserts the exact solver matches/beats SLSQP, is deterministic, and is exit-status-independent.
- `SEED=42 bash scripts/check.sh` re-verified green this session: ALL CHECKS PASSED, all experiment-script imports OK.

I started the optional `--extended` verification run (the next session's bounded task), then stopped it after ~1 min and restored the goldens, because leaving a half-finished verification run violates the baseline-integrity rule. The interrupted run had dirtied `experiments/blend_tsm_dnlowbeta_large_liquid.json` and left an `ACTIVE.json` snapshot; `--restore-only` cleaned both. **The extended run was not completed this session — it remains to be run.**

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
```