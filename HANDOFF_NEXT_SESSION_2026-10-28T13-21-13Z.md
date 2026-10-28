# Handoff: Next Agentic Session — 2026-10-28T13-21-13Z

> **START HERE.** Repository is fully verified and stable. Your initial task is to verify stability by running `scripts/check.sh` and the extended verification suite, confirm the pre-existing known drifts remain unchanged, and report results. Do not modify goldens, weaken tolerances, or change any gate logic. If interrupted during verification, recover with `SEED=42 python3 run_all_verification.py --restore-only`. Follow all constraints below.

---

## Current state (at handoff time)
- **HEAD:** 2ff896e chore(kilo): checkpoint agent session
- **Branch:** main
- **Working tree:** only `__pycache__/*.pyc` modifications (gitignored; ignore them). No tracked source/data changes.
- **Research phase complete** (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **No live verification snapshot** (`.verify_snapshot/` absent). No run in progress; nothing to recover.

## Known pre-existing drift (reporting-only; decisions unchanged)
- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). Three structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.

## Initial task for the next session
1. **Verify repo health (fast, offline):**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect ALL CHECKS PASSED.

2. **Run the extended verification suite (bounded):**
   ```bash
   SEED=42 python3 run_all_verification.py --extended
   ```
   Expect only the pre-existing E030/E041 drift above. Do **not** weaken tolerances, skip drivers, or modify committed goldens. If interrupted for any reason, recover with:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```

3. **Report results:** Summarize `check.sh` outcome, extended verification summary (especially E030/E041), and explicitly confirm drift status unchanged. Flag any new structural anomalies — do **not** re-pin or change tolerances; report them.

## Constraints
- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

## Suggested first commands
```bash
git status --short
git log -1 --oneline
SEED=42 bash scripts/check.sh
```

**End of handoff.**
