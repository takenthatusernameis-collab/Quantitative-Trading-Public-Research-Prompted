# Handoff for Next Agentic Work Session

**Created:** 2026-10-28T07:27:45Z
**Durable handoff target:** `HANDOFF_NEXT_SESSION_2026-10-28T07-27-45Z.md` (this file; also pointed to by `HANDOFF_CURRENT.md`).
**Supersedes:** `HANDOFF_NEXT_SESSION_2026-10-28T07-27-33Z.md` (most recent in this sequence)

## Initial Task Message for Next Agentic Work Session

Repo state is clean and verified as of this handoff. No bounded research task is pre-assigned for the next session — this is a continuation handoff. Start with the quick health check, then act only on assigned work.

### Quick verification (do first)
```bash
SEED=42 bash scripts/check.sh
```
Expected: `ALL CHECKS PASSED`. If anything fails, recover before committing (see recovery rules).

### Current baseline (at creation time)
- HEAD = `76931c5`, branch `main`, up to date with `origin/main` (if tracking)
- Working tree: only `__pycache__/*.pyc` modified (gitignored — ignore). No tracked source/data/golden changes.
- No live verification snapshot (`.verify_snapshot/` absent). Guards pass (golden baseline + data coverage + goldens clean).
- Research phase complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`.

### Priority tasks
1. **Health check** — Run `SEED=42 bash scripts/check.sh`. Confirm guards pass.
2. **Review ledger** — Skim `ledger/RESEARCH_LEDGER.md` for open items (especially E041 numeric drift tolerance discussion; E029/E030 reproducibility notes). Decide if action needed.
3. **Only act on assigned work** — No bounded task is pre-assigned. If the user has a specific experiment/task, load its `E*_TASK_SPEC.md` and follow pre-registration/promotion gates.

### If starting a new bounded research task
- Create/update driver `experiments/run_eXXX.py` with a `pre_registered` block (gates, falsification expectations, sensitivity grid) before running.
- Run with `SEED=42`. Preserve negative results honestly (REJECTED/PARTIAL).
- Verify with `SEED=42 python3 run_all_verification.py` (or targeted runs). Do **not** re-pin goldens to silence numeric drift — document in ledger.
- Update `ledger/RESEARCH_LEDGER.md` if promoting/rejecting.

### Recovery & safety rules
- Always use `SEED=42`.
- If verification interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` if appropriate).
- Never leave a verification run half-finished; `.verify_snapshot/` is recoverable but must be cleared properly.
- Cache coverage enforced (`scripts/check_data_coverage.py`). Add pinned data + re-pin via `--update` if introducing new inputs.
- Golden baseline enforced (`scripts/check_golden_baseline.py`) — re-pin only with explicit intent and document.
- Extended drift (E029/E030/E041) is documented; do not weaken tolerances or modify committed goldens to "fix" environment drift.

### Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities/futures/macro. Pre-registered experiments, multiple-testing discipline, goldens are canonical.
(End of file)
