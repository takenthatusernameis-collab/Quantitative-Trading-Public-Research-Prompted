# Agentic Work Session Handoff

**Created:** 2026-11-23T15:24:43Z
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Status:** READY FOR NEXT SESSION

## Initial Task

Continue quantitative-strategy research work on this repository. Before running anything:

1. Read `AGENTS.md` — it defines the verification suite, golden baseline rules, reproducibility conventions, and CI gate notes.
2. Confirm `experiments/*.json` are intact (they may have been overwritten by an interrupted verification run). If so, restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) to verify conventions + goldens are clean.
4. Pick up work from `ledger/RESEARCH_LEDGER.md` (E001–E043 complete; see ledger for dispositions and pending items).

## Key Conventions

- Always use `SEED=42`.
- Never commit verification output; restore goldens before committing.
- `experiments/*.json` are canonical artifacts; do not re-pin goldens except via `python3 scripts/check_golden_baseline.py --update` and record in the ledger.
- Data inputs are pinned; adding a new one requires committing the file and re-pinning with `python3 scripts/check_data_coverage.py --update`.
- CI verification-gate workflow cannot be created by automated agents; see `.github/workflow-templates/verification-gate.yml` and `VERIFICATION_GATE_TEMPLATE.md`.

## Commands

- `SEED=42 bash scripts/check.sh` — convention robustness + template validation (~seconds)
- `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — extended verification (~21 min)
- `python3 -m py_compile <file>` — syntax check on changed Python files
