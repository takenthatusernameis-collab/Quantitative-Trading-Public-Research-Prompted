# Durable Handoff — Initial Task Message

**Created:** 2026-11-10T21:38:11Z
**Session:** prior agentic work session
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Context

This is a quantitative-strategy research repository on 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043); surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

Key conventions (see `AGENTS.md`):
- `experiments/*.json` are canonical committed research artifacts — never leave them half-finished or committed after a verification run.
- Seed: always `SEED=42`.
- Drivers run offline with `QUANT_RESEARCH_OFFLINE=1`; every `data.download()` input must be pinned and cache-covered (`ledger/data_baseline.json`).
- No separate linter; run `python3 -m py_compile` on changed files.
- `make check`, `make verify-quick`, `make verify-extended`, `make verify-full` are the local CI equivalents.

## Open item for next session

**E041 optimizer drift is still open.** Per `AGENTS.md` ledger entries E048/E049:
- `src/portfolio_opt.py` validates solver answers on the problem's constraints, never on solver exit status (fixes the scipy-build-dependent SLSQP status-8 gating).
- The tangency QP remains ill-conditioned: a 1-ulp input perturbation moves `min_var` answers by ~1e-05, so E041/E042 grid artifacts still drift by 29–133 differences exceeding the 1e-4 tolerance.
- **Do not re-pin** E041/E042 goldens to silence drift — see the open item in `ledger/RESEARCH_LEDGER.md`.

Suggested first step for the next session: inspect `ledger/RESEARCH_LEDGER.md` for the E041/E042 open item and decide whether to (a) investigate conditioning/solver stability in `src/portfolio_opt.py`, or (b) document the drift as accepted and close the item.

## Immediate commands available

```bash
SEED=42 bash scripts/check.sh          # convention robustness + template validation
SEED=42 python3 run_all_verification.py --verify-quick   # 8-driver quick re-execution
python3 -m py_compile src/*.py experiments/*.py          # syntax check on changed files
```
