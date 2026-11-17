# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-17T23:38:54Z
**HEAD:** `50ff2043bdbf03005cfb68bc42a3fcaf61943e21` (main, 2026-11-17 23:38:31 +0000) "chore(kilo): checkpoint agent session"
**Branch:** `main` (in sync with `origin/main`, `git rev-list --left-right --count origin/main...HEAD` → `0	0`)
**Prior handoff:** `handoff_2026-11-17T23-38-31Z_INITIAL_TASK.md` — superseded by this file.

## Repository state (at capture)

- **Research phase:** COMPLETE (E001–E043/E051 recorded in `ledger/RESEARCH_LEDGER.md`). No new research was performed in this session. Surviving validated strategies and open caveats remain as documented in the ledger.
- **Working tree:** source-clean. `git status` shows only 15 modified tracked `__pycache__/*.pyc` build artifacts under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/` — **do not commit**. No tracked diffs in `experiments/`, `data/`, `ledger/`, `scripts/`, `src/`, `tests/`, or `research_state/`.
- **Golden baseline:** 107 tracked artifacts under `experiments/`, matching HEAD. No `.verify_snapshot/` and no `.verify_reports/` present; no interrupted verification run indicated.
- **Canonical handoff aliases:** repointed by `python3 scripts/repoint_handoff.py handoff_2026-11-17T23-38-54Z_INITIAL_TASK.md` after this file was written.

## Canonical invariants (do not violate)

- `experiments/*.json` are golden artifacts. Verification overwrites them during runs and restores them afterward — **never leave a run half-finished**.
- If interrupted or on golden/baseline mismatch: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD still holds the pinned baseline). See `AGENTS.md` "Baseline Integrity".
- Re-pin `experiments/` or `data/` baselines only via explicit documented `--update` flows (`python3 scripts/check_golden_baseline.py --update`, `python3 scripts/check_data_coverage.py --update`), never as a side effect of verification.
- Always use `SEED=42` for verification/reproduction commands.
- Do not commit `__pycache__/*.pyc` artifacts or verification output.
- Do not modify `.github/workflows/` via automation (template: `.github/workflow-templates/verification-gate.yml`).

## Known open items (not blockers)

- **E049/E050:** E041/E042 grid artifacts remain 1-ulp sensitive under the ill-conditioned tangency QP (optimizer constraint-validation defect fixed; exact KKT enumeration routes the QP per E050). Numeric drift remains in extended comparison — do **not** re-pin to silence drift.
- **E048:** data-cache coverage is enforced; `scripts/check_data_coverage.py` guards every `data.download()` call site. To add a data input, commit the file and re-pin via `--update`.
- CI verification workflow cannot be pushed by automated agents; maintainer action required per `.github/workflow-templates/verification-gate.yml` and `VERIFICATION_GATE_TEMPLATE.md`.

## Recommended next actions

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` is clean aside from `__pycache__/*.pyc` noise and that no `.verify_snapshot/` exists.
2. **Integrity check (before new work):** run `SEED=42 bash scripts/check.sh` (or `make check`). If a golden/baseline mismatch is reported, restore per `AGENTS.md` before proceeding. Escalate to `SEED=42 python3 run_all_verification.py` / `--extended` only if required.
3. **Handle user requests:** follow project conventions (pre-registration, no goalpost changes, no committing verification output, no golden/data re-pins without deliberate update flow). Research program is closed per ledger — avoid speculative new strategy exploration unless explicitly directed and properly pre-registered.
4. **Session close-out (if material work is done):** create a new timestamped durable handoff, repoint canonical aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`, update `ledger/RESEARCH_LEDGER.md` only if appropriate, and do not commit `__pycache__` artifacts.

_No pending implementation tasks carried forward from this handoff._
