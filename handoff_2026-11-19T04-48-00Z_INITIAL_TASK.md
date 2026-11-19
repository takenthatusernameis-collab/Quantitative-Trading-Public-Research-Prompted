# Agentic Work Session Handoff

**Created:** 2026-11-19T04:48:21Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Status:** Open — awaiting next agentic work session

## Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session

No specific task was provided in the opening message other than to leave this handoff. Before doing any work:

1. Read `AGENTS.md` fully (project commands, baseline integrity, reproducibility, conventions).
2. Check `git status` and `git log --oneline -10` to confirm the working tree is clean and no interrupted verification run left driver output in `experiments/`.
3. If a verification run was interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` before committing anything.
4. The canonical artifacts are `experiments/*.json`; they are overwritten by the verification suite and restored afterwards — never leave a run half-finished.

## Common commands (run with SEED=42)

- Fast check: `SEED=42 bash scripts/check.sh` (or `make check`)
- Quick verify (~8 min): `SEED=42 python3 run_all_verification.py` (or `make verify-quick`)
- Extended verify (~21 min): `SEED=42 python3 run_all_verification.py --extended`
- Full verify (~15 min): `SEED=42 python3 run_all_verification.py --full`
- Convention robustness only: `SEED=42 python3 verify_convention_robustness.py`

## Key rules

- `QUANT_RESEARCH_OFFLINE=1` is set by the verification suite; unpinned data inputs fail hard.
- Never commit verification output; restore goldens before committing.
- `cvxpy`/`cvxopt` optional; optimizer falls back to `scipy.optimize`.
- No separate linter; run `python3 -m py_compile` on changed files.
- CI verification-gate workflow cannot be created by automated agents; template at `.github/workflow-templates/verification-gate.yml`.
