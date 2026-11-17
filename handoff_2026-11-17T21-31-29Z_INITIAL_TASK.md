# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-17T21:31:29Z
**HEAD:** `4d93fa5b440c038e9bdca00eb3b2ff95d7dc7662` (main)
**Branch:** `main` (in sync with `origin/main`)
**Prior handoff:** `handoff_2026-11-17T21-28-38Z_INITIAL_TASK.md` — superseded by this file.

## Repository state (at capture)

- **Research phase:** COMPLETE. Experiments E001–E051 recorded in `ledger/RESEARCH_LEDGER.md`; no new research performed in this session. All subsequent ledger entries (E052–E112) are durable-handoff refreshes only.
- **Working tree:** source-clean aside from 12 modified tracked `__pycache__/*.pyc` bytecode files (build artifacts, not source — do not commit). No material changes in `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, or ledger sources.
- **Golden baseline:** 138 tracked artifacts under `experiments/`, all matching HEAD.
- **Verification state:** no `.verify_snapshot/` and no `.verify_reports/` present; no interrupted verification run indicated; nothing to recover.
- **Symlink tree:** generic canonical pointers repointed to this file via `scripts/repoint_handoff.py`.

## Canonical invariants (do not violate)

- `experiments/*.json` are golden artifacts. Verification overwrites them during runs and restores them afterward — **never leave a run half-finished**.
- If interrupted or on golden mismatch: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD still holds the pinned baseline). See `AGENTS.md` "Baseline Integrity".
- Re-pin `experiments/` or `data/` baselines only via explicit documented `--update` flows, never as a side effect of verification.
- Always use `SEED=42` for verification/reproduction commands.
- Do not commit `__pycache__/*.pyc` artifacts or verification output.

## Known open items (from ledger; not blockers)

- **E049/E050:** E041/E042 grid artifacts remain 1-ulp sensitive under the ill-conditioned tangency QP. Do **not** re-pin to silence drift.
- **E048:** data-cache coverage is an enforced invariant; `scripts/check_data_coverage.py` guards every `data.download()` call site.
- CI verification workflow cannot be pushed by automated agents; maintainer action required.

## Recommended next actions

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` is clean aside from regenerated `__pycache__/*.pyc` noise and that no `.verify_snapshot/` exists.
2. **Integrity check (before new work):** run `SEED=42 bash scripts/check.sh` (or `make check`).
3. **Handle user requests:** follow project conventions. Research program is closed per ledger (E001–E051); avoid speculative new strategy exploration unless explicitly directed and properly pre-registered.
4. **Session close-out (if material work is done):** create a new timestamped durable handoff, repoint canonical handoff aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`, and do not commit `__pycache__` artifacts.

_No pending implementation tasks carried forward from this handoff._
" filePath">
/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/handoff_2026-11-17T21-31-29Z_INITIAL_TASK.md