# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-31T18:49:57Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** `7303475` (chore(kilo): checkpoint agent session)
**Working tree:** clean at handoff time. No live verification run in progress; `.verify_snapshot/` absent.

## Initial Task (Start Here)

**Task:** Repository is fully verified and in a stable state. No new research is warranted. Verify stability by running the baseline integrity check, confirm the pre-existing known drifts remain unchanged, and report results. Do not modify goldens, weaken tolerances, or change any gate logic. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json` via `.verify_snapshot/`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- Do not re-pin goldens without ledger justification.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

## Quick reference

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
```

## Known pre-existing drift (reporting only; do not re-pin)

- **E041**: residual numeric diffs from 1-ulp sensitivity of the ill-conditioned tangency QP.
- **E030**: numeric diffs on near-zero quantities.
- **E042 lead**: `/primary` reproduces to 5e-9; `/placebo_constrained` was deliberately re-pinned (still below the G2 bar of 3.0, so `decision` REJECTED 4/5 is unchanged).

## Open item from the ledger (E049 follow-up)

The tangency QP in `src/portfolio_opt.py` is still ill-conditioned. Tightening `exact_qp` internal tolerances (and removing the conditional ridge/projection) is the documented next step, but must be done as a **deliberate re-pin** with `python3 scripts/check_golden_baseline.py --update`, never as a silent side effect of a verification run.
