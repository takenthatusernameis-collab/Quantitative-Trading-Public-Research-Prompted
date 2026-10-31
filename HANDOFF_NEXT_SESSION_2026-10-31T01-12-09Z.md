# Handoff — Quantitative Trading Research

**Timestamp:** 2026-10-31T01:17:00Z

## Initial task for the next session

Leave a timestamped, clear initial task message for the next agentic work session in a durable handoff (this file).

## Project context

Repo: Quantitative-Trading-Public-Research-Prompted
Root: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. `experiments/*.json` are committed canonical research artifacts — never modified by verification.

## Common commands

```bash
SEED=42 bash scripts/check.sh           # convention-robustness check + template validation (~seconds, offline)
SEED=42 python3 run_all_verification.py --skip-slow   # quick full verification (~8 min)
python3 -m py_compile <changed-file>    # lint/typecheck equivalent (no separate linter configured)
```

## Baseline integrity rules

- A verification run backs up `experiments/` to `.verify_snapshot/` and restores them afterward — never leave a run half-finished.
- Do not commit verification output or re-pin goldens as a side effect of running the suite.
- `scripts/check_goldens_clean.py` fails when a tracked artifact under `experiments/` differs from HEAD.
- `scripts/check_golden_baseline.py` compares artifacts against SHA-256 fingerprints in `ledger/golden_baseline.json`.

## Open items (from AGENTS.md / ledger)

- E041 optimizer determinism: 133 remaining numeric differences (1-ulp QP sensitivity) still exceed the 1e-4 tolerance in the extended block; do not re-pin to silence it. Open item in ledger.
- E042 min-var confirmatory (PARTIAL).

## Notes

- Seed: always use `SEED=42`.
- Offline: `QUANT_RESEARCH_OFFLINE=1` is used by the verification suite; missing cache entries fail hard.
- CI workflow `.github/workflows/verification-gate.yml` cannot be created by automated agents; template at `.github/workflow-templates/verification-gate.yml`.