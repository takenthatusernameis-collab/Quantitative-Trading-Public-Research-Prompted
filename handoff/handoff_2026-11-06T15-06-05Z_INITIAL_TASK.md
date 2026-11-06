# Handoff — agentic work session

**Timestamp:** 2026-11-06T15:06:05Z
**Session:** Kilo (kilo/kilo-auto/free)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` / `ecab5b8` (`chore(kilo): checkpoint agent session`)
**Working tree:** clean at handoff creation (no tracked/untracked changes observed via `git status --short`)
**`.verify_snapshot/`:** absent (no interrupted verification run to recover)

## Repository state
- Research phase complete (E001–E092/E077 context per ledger/history; see `ledger/RESEARCH_LEDGER.md` for authoritative status).
- Canonical experiment artifacts live in `experiments/*.json`; they are golden/baseline-sensitive and must not be modified as a side effect of verification or ad-hoc runs.
- Prior handoff reviewed: `handoff/handoff_2026-11-06T15-01-46Z_INITIAL_TASK.md`.

## Clear initial task for next session
1. **Integrity check (first action, only if appropriate for the session):** run the fast offline check to confirm goldens/baseline/conventions are intact before any new work:
   ```bash
   SEED=42 bash scripts/check.sh
   # or
   make check
   ```
2. **If `check.sh` passes:** treat the repository as steady/closed unless the user gives an explicit new task. Do not start new research, re-pin baselines, or run long verification by default.
3. **If `check.sh` reports a golden/baseline mismatch:** stop and fix before committing. Follow `AGENTS.md` “Baseline Integrity”. Never capture verification output as the new baseline. Recovery: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts as documented).
4. **If explicitly asked to start new research:** pre-register as the next experiment (E093+), document gates/falsification/sensitivity before execution, use `SEED=42`, respect offline/cache/baseline guards, record negative results honestly, and update `ledger/RESEARCH_LEDGER.md` with evidence.

## Useful commands (run only when explicitly requested)
```bash
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # extended (~21 min)
SEED=42 python3 run_all_verification.py --full       # full (~15 min, heavier E042/grid)
SEED=42 python3 run_all_verification.py --skip-slow
SEED=42 python3 run_all_verification.py --restore-only
```

## Guardrails
- Use `SEED=42` for reproducible runs.
- Do **not** commit verification output or modify `experiments/*.json` goldens unintentionally.
- Do **not** re-pin `ledger/golden_baseline.json` / `ledger/data_baseline.json` as a side effect of verification.
- Do **not** commit unless explicitly asked.
- CI workflow `.github/workflows/verification-gate.yml` cannot be created by automated agents; maintainers must copy `.github/workflow-templates/verification-gate.yml` via GitHub UI.
