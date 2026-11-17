# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-17T21:49:08Z
**HEAD:** `76ffae766db37a665ab97139e2cf43dae0f4c00a` (main, 2026-11-17 21:48:44 +0000) "chore(kilo): checkpoint agent session"
**Branch:** `main` (in sync with `origin/main`; `git rev-list --left-right --count origin/main...HEAD` → `0 0`)
**Prior handoff:** `handoff_2026-11-17T21-45-25Z_INITIAL_TASK.md` — superseded by this file.

## Initial task (do this first)

> **Task:** Take over the quantitative-strategy research repository as the next agentic work session. The research program is closed (E001–E051) and the working tree is source-clean; your job is to (1) orient from this handoff and `AGENTS.md`, (2) re-verify repository integrity with `SEED=42 bash scripts/check.sh`, (3) address any user request under the project's pre-registration and baseline-integrity rules, and (4) if material work is done, leave a fresh timestamped durable handoff and repoint the canonical aliases with `python3 scripts/repoint_handoff.py <new_handoff_file>`. Do **not** re-pin golden/data baselines, commit verification output, or commit `__pycache__/*.pyc` as a side effect of verification.

## Repository state (at capture)

- **Research phase:** COMPLETE. Experiments E001–E051 recorded in `ledger/RESEARCH_LEDGER.md`; no new research performed in this session. Ledger tail confirms closure through E466 (durable-handoff refresh, 2026-11-17T19:33:44Z); E464–E466 are handoff/bookkeeping entries only.
- **Working tree:** source-clean. `git status` shows only 12 modified tracked `__pycache__/*.pyc` bytecode files under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/` (build artifacts, not source — do not commit). `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/` is empty once `__pycache__` is excluded.
- **Golden baseline:** 138 tracked artifacts under `experiments/`, all matching HEAD. `scripts/check_golden_baseline.py` pins 107 artifacts by SHA-256; no re-pin has been performed.
- **Verification state:** no `.verify_snapshot/` and no `.verify_reports/` present; no interrupted verification run indicated; nothing to recover.
- **Symlink tree:** generic canonical aliases (root, `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`) all resolve to this handoff after repoint. Timestamped/historical aliases are intentionally left untouched per `scripts/repoint_handoff.py` history-preservation policy.

## Canonical invariants (do not violate)

- `experiments/*.json` are golden artifacts. Verification overwrites them during runs and restores them afterward — **never leave a run half-finished**.
- If interrupted or on golden mismatch: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD still holds the pinned baseline). See `AGENTS.md` "Baseline Integrity".
- Re-pin `experiments/` or `data/` baselines only via explicit documented `--update` flows (`python3 scripts/check_golden_baseline.py --update`, `python3 scripts/check_data_coverage.py --update`), never as a side effect of verification.
- Always use `SEED=42` for verification/reproduction commands.
- Do not commit `__pycache__/*.pyc` artifacts or verification output.

## Known open items (from ledger; not blockers)

- **E049/E050:** E041/E042 grid artifacts remain 1-ulp sensitive under the ill-conditioned tangency QP (optimizer constraint-validation defect fixed; exact KKT enumeration routes the QP per E050). Numeric drift remains in the extended comparison. Do **not** re-pin to silence drift.
- **E048:** data-cache coverage is an enforced invariant; `scripts/check_data_coverage.py` guards every `data.download()` call site. To add a data input, commit the file and re-pin via `--update`.
- CI verification workflow cannot be pushed by automated agents; maintainer action required per `.github/workflow-templates/verification-gate.yml` and `VERIFICATION_GATE_TEMPLATE.md`.

## Recommended next actions

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` is clean aside from regenerated `__pycache__/*.pyc` noise and that no `.verify_snapshot/` exists.
2. **Integrity check (before new work):** run `SEED=42 bash scripts/check.sh` (or `make check`). If a golden/baseline mismatch is reported, restore per `AGENTS.md` before proceeding. Escalate to `SEED=42 python3 run_all_verification.py` / `--extended` only if required.
3. **Handle user requests:** follow project conventions (pre-registration, no goalpost changes, no committing verification output, no golden/data re-pins without deliberate update flow). Research program is closed per ledger (E001–E051); avoid speculative new strategy exploration unless explicitly directed and properly pre-registered.
4. **Session close-out (if material work is done):** create a new timestamped durable handoff, repoint canonical handoff aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`, update `ledger/RESEARCH_LEDGER.md` only if appropriate, and do not commit `__pycache__` artifacts.

_No pending implementation tasks carried forward from this handoff._