# Durable Handoff — Next Agentic Work Session

**Generated:** 2026-10-30T12:35:46Z (UTC)
**Session:** handoff for next agentic work session
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**Last commit:** b5dc429 chore(kilo): checkpoint agent session

---

## INITIAL TASK (do first)

No specific technical task was assigned in this turn. The working tree is clean except untracked `__pycache__/*.pyc` build artifacts. No verification snapshot is active.

1. **Confirm repo state before anything else**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match, data coverage, portfolio_opt tests.

2. **If checks fail**
   - Goldens differ from HEAD → restore from the commit whose SHA-256 matches `ledger/golden_baseline.json` (or `SEED=42 python3 run_all_verification.py --restore-only`).
   - Never re-pin to silence drift; re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff.

3. **Then idle awaiting explicit user direction.**
   - Do NOT make source changes or commits unless explicitly asked.
   - Do NOT modify `experiments/*.json` goldens as a side effect of verification.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **Working tree:** clean except `__pycache__/*.pyc` (untracked build artifacts, not committed).
- **No uncommitted source changes.** No verification snapshot active in `.verify_snapshot/`.
- `experiments/*.json` goldens match HEAD (no captured verification output pending).

## Known open items (read AGENTS.md before acting)

- Optimizer determinism (E049): `src/portfolio_opt.py` validates solver answers on constraints, never exit status; pinned by `tests/test_portfolio_opt.py`. E041/E042 grid artifacts still drift by 29–133 differences (ill-conditioned QP). Do NOT re-pin to silence.
- E041 drift root-caused (ledger E049): 3 structural diffs gone, 133 numeric remain; open item in ledger.
- Cache coverage enforced (E048): `scripts/check_data_coverage.py` validates all data inputs are pinned in `ledger/data_baseline.json`.

## Key commands

- `SEED=42 bash scripts/check.sh` — convention-robustness + template validation (~seconds, offline)
- `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — extended (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — full (~15 min)
- `SEED=42 python3 run_all_verification.py --restore-only` — recover goldens after interrupted run
- `python3 -m py_compile` on changed files (no separate linter)

## Notes

- `AGENTS.md` is the source of truth for commands/conventions; re-read before running the verification suite.
- The CI gate workflow cannot be created by automated agents (template at `.github/workflow-templates/verification-gate.yml`).

(End of file)
