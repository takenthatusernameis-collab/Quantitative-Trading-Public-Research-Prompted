# Handoff — agentic work session

**Created:** 2026-11-21T22:12:36Z
**Repo:** Quantitative-Trading-Public-Research-Prompted

## Pending task

No active task. Await next instruction.

## Environment notes

- Python research repo; verify via `SEED=42 bash scripts/check.sh` (`make check`) or `make verify-quick` (~8 min).
- `experiments/*.json` are canonical research goldens — never commit verification output.
- Optional deps: `cvxpy`/`cvxopt`; optimizer falls back to `scipy.optimize`.
- Offline drivers run with `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard.

## Conventions

- Seed: `SEED=42`. Close-to-close is v1.2.3 primary convention.
- No separate linter; run `python3 -m py_compile` on changed files.
- Do not auto-create `.github/workflows/verification-gate.yml` (controller restores it / token lacks push). Use `.github/workflow-templates/verification-gate.yml` template via maintainer UI.
