# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-29T22:43:30Z (message time)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `ac21627` (chore(kilo): checkpoint agent session), up to date with `origin/main`

## State

Research phase complete (E001–E043). Surviving validated strategies documented in
`ledger/RESEARCH_LEDGER.md`. Baseline integrity guards enforced. Working tree
clean of tracked source/data changes; only `__pycache__/*.pyc` show as modified
(they are force-tracked in git — pre-existing, not in scope). No `.verify_snapshot/`
active; no interrupted run to recover.

## Initial Task (Start Here)

Verify the baseline is clean before any work.

1. Run `SEED=42 bash scripts/check.sh` — all guards must pass with no golden diffs.
2. Run `git status --short` / `git diff --name-only` — confirm clean tree.
3. If an interrupted verification left dirty `experiments/*.json`, restore:
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).

Do not re-pin goldens to silence drift. Keep committed goldens authoritative.
Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` first.

## Known Open Items (Do Not "Fix" By Re-Pinning)

- **E041 numeric drift (open):** Optimizer determinism issue (ledger E049) fixed
  gating on solver status, but the tangency QP remains ill-conditioned. Extended
  verification still reports ~133 numeric differences for E041; **do not re-pin
  `experiments/e041_*.json`**. See `ledger/RESEARCH_LEDGER.md` (E049).
- **E042 grid artifacts:** Similar 1-ulp sensitivity can appear in the E042
  sensitivity grid. Do not re-pin goldens to force a match.
- **E030:** numeric diffs on near-zero quantities (documented). Do not re-pin.
- **Data coverage:** Inputs must remain tracked and pinned in
  `ledger/data_baseline.json`. If adding a new data file, commit it and run
  `python3 scripts/check_data_coverage.py --update` deliberately (never as a
  side-effect of `run_all_verification.py`).
- **Pinned fundamentals/vintages:** `data/fundamentals/` (per
  `data/fundamentals_vintages.json`) and `data/vintages.json` are part of
  reproducibility. Treat as canonical.

## Recommended Next Research-Engineering Task

Replace SLSQP QP solves in `src/portfolio_opt.py` with a well-conditioned,
deterministic solver (for N <= 5, exact active-set enumeration of all KKT
points is feasible and already used as a reference oracle), then deliberately
re-pin affected artifacts. See ledger E049 and the `src/portfolio_opt.py:253`
start-point defect (negative-denominator masking; deliberately left unfixed
because fixing it changes published numbers and requires a deliberate re-pin).

## Quick Commands

```bash
# Fast gate
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
```