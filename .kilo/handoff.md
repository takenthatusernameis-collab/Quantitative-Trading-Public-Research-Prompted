# Durable Handoff — Initial Task Message

**Created:** 2026-10-29T10:27:00Z
**Session:** Kilo coding session
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state

No active code change in progress. Repository is a quantitative-strategy research project (2014–2026 US equities, futures, macro). Verification suite: `scripts/check.sh` (fast, offline) / `run_all_verification.py` (quick/extended/full). Committed experiment goldens live under `experiments/*.json`; do not commit verification output.

Research phase COMPLETE (E001–E049); E049 is the last experiment.
- E049 fixed `src/portfolio_opt.py` tangency-QP determinism (judge answers on QP constraint feasibility, not scipy `res.success` exit status); added `tests/test_portfolio_opt.py` (5 tests); re-pinned `experiments/e042_lead_config_confirmatory.json` golden.
- Primary gate `SEED=42 python3 run_all_verification.py` is GREEN.

Working tree clean except regenerated `__pycache__/*.pyc` bytecode.

## Next task (initial)

No specific objective assigned. Establish a clean baseline before any changes:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If green, proceed only when a concrete objective is provided. Then read relevant drivers/tests, make minimal changes, run `python3 -m py_compile` on modified files, and run the applicable verification (`check`/`verify-quick`/`verify-extended`).

## Notes

- Never leave a verification run half-finished (it overwrites `experiments/*.json` then restores). If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Drivers run offline via `QUANT_RESEARCH_OFFLINE=1`; missing cached inputs fail hard.
- Lint: `python3 -m py_compile` on changed Python files. No separate linter configured.
- Do not commit or modify golden artifacts without explicit user request.

## Open items (documented, not fixed)

- Ill-conditioned tangency/min-var QP (~2.6e-05 weight drift under 1-ulp perturbation).
- `y0 = w_feas / max(mu_s'w_feas, 1e-12)` negative-denominator mask at `src/portfolio_opt.py:253`.
- Both left for deliberate re-pin decision; see `ledger/RESEARCH_LEDGER.md`.

(End of file)
