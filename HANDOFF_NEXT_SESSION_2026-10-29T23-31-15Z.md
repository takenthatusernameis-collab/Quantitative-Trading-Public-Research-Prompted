# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-29T23:31:15Z (message time)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ fd721c8 (up to date with origin/main)

## State
Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Baseline integrity guards enforced. Working tree clean at handoff time.

## Initial Task (Start Here)
Verify baseline integrity before any changes:

1. `SEED=42 bash scripts/check.sh` — all guards must pass, no golden diffs.
2. `git status --short && git diff --name-only` — confirm clean.
3. If interrupted verification left dirty `experiments/*.json`, restore with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).

Do not re-pin goldens to silence drift. Keep committed goldens authoritative. Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` first.

## Known Open Items (Do Not "Fix" By Re-Pinning)
- **E041 numeric drift (open):** Optimizer determinism fixed (ledger E049) but tangency QP remains ill-conditioned. Extended verification still reports ~133 numeric differences for E041; do **not** re-pin `experiments/e041_*.json`. See `ledger/RESEARCH_LEDGER.md` (E049).
- **E042 grid artifacts:** Possible 1-ulp sensitivity; do not re-pin goldens to force match.
- **Data coverage:** Inputs must remain tracked/pinned in `ledger/data_baseline.json`. If adding data, commit and run `python3 scripts/check_data_coverage.py --update` deliberately (never as side effect of `run_all_verification.py`).
- **Pinned fundamentals/vintages:** `data/fundamentals/` (per `data/fundamentals_vintages.json`) and `data/vintages.json` are canonical.

## Recommended Next Research-Engineering Task
Replace SLSQP QP solves in `src/portfolio_opt.py` with a well-conditioned, deterministic solver (for N<=5, exact active-set enumeration of all KKT points is feasible and already used as reference oracle), then deliberately re-pin affected artifacts. See ledger E049 and `src/portfolio_opt.py:253` start-point defect.

## Quick Commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py        # quick
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --restore-only
```
