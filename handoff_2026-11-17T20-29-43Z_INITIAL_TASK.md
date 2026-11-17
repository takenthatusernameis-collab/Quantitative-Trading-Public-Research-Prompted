# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-17T20:29:43Z
**HEAD:** `02ef97c8d5345125a8cbfc3e84ea455c4792a519` (main)
**Branch:** `main`
**Prior handoff:** `handoff_2026-11-17T20-28-41Z_INITIAL_TASK.md` — superseded by this file.

## Repository state (at capture)

- **Research phase:** COMPLETE. Experiments E001–E051 are recorded in `ledger/RESEARCH_LEDGER.md`; no new research performed in this session.
- **Working tree:** source-clean except regenerated `__pycache__/*.pyc` bytecode noise (untracked/modified, not source). No material changes in `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, or ledger sources.
- **Verification state:** no `.verify_snapshot/` or `.verify_reports/` present; no interrupted verification run indicated.
- **Delta vs prior handoff:** handoff refresh only; no experiment/data/src/test/script/research_state changes.

## Canonical invariants (do not violate)

- `experiments/*.json` are golden artifacts. Verification overwrites them during runs and restores them — **never leave a run half-finished**.
- If interrupted or on golden mismatch: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD still holds the pinned baseline). See `AGENTS.md` "Baseline Integrity".
- Re-pin `experiments/` or `data/` baselines only via explicit documented `--update` flows, never as a side effect of verification.
- Always use `SEED=42` for verification/reproduction commands.

## Known open items (from ledger; not blockers)

- **E049:** E041/E042 grid artifacts remain 1-ulp sensitive under the ill-conditioned tangency QP (optimizer constraint-validation defect fixed; numeric drift remains in extended comparison). Do **not** re-pin to silence drift.
- CI verification workflow cannot be pushed by automated agents; maintainer action required per `.github/workflow-templates/verification-gate.yml` and `VERIFICATION_GATE_TEMPLATE.md`.

## Recommended next actions

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` is clean aside from regenerated `__pycache__/*.pyc` noise and that no `.verify_snapshot/` exists.
2. **Integrity check (before new work):** run `SEED=42 bash scripts/check.sh` (or `make check`). If a golden/baseline mismatch is reported, restore per `AGENTS.md` before proceeding. Escalate to `SEED=42 python3 run_all_verification.py` / `--extended` only if required.
3. **Handle user requests:** follow project conventions (pre-registration, no goalpost changes, no committing verification output, no golden/data re-pins without deliberate update flow). Research program is closed per ledger (E001–E051); avoid speculative new strategy exploration unless explicitly directed and properly pre-registered.
4. **Session close-out (if material work is done):** create a new timestamped durable handoff, repoint canonical handoff aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`, update `ledger/RESEARCH_LEDGER.md` only if appropriate, and do not commit `__pycache__` artifacts.

_No pending implementation tasks carried forward from this handoff._
