# Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-10-29T19:54:28Z
**Status:** Initial task message (durable handoff)

## Initial Task

Verify baseline integrity before any further work:

```bash
SEED=42 bash scripts/check.sh
```

(or `make check`). This is the fast, offline, convention-robustness gate (py_compile, import checks, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, template validation). Confirm it passes.

If a previous verification run was interrupted and left driver output instead of committed goldens, recover first:

```bash
SEED=42 python3 run_all_verification.py --restore-only
```

then re-run `scripts/check.sh`.

## Context

- Research phase complete (E001–E043); surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are canonical committed artifacts — never modify as a side effect of verification. Re-pinning requires `scripts/check_golden_baseline.py --update` with explicit justification.
- Data coverage invariant: all `data.download()` inputs must be committed and pinned in `ledger/data_baseline.json`; runs execute offline (`QUANT_RESEARCH_OFFLINE=1`).
- Known reporting-only drifts (do not re-pin, do not weaken tolerances): E030 (near-zero quantities), E041 (~133 numeric diffs from ill-conditioned QP, optimizer determinism fixed per ledger E049). E041's structural differences are gone; decision (REJECTED 3/5) unchanged.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (suite backs up/restores `experiments/*.json` via `.verify_snapshot/`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

(End of file)
