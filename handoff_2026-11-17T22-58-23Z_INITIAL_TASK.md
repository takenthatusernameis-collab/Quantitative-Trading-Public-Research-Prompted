# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-17T22:58:23Z
**HEAD:** `c6cab460` (main, 2026-11-17 22:56:00 +0000) "chore(kilo): checkpoint agent session"
**Branch:** `main` (in sync with `origin/main`)
**Prior handoff:** `handoff_2026-11-17T22-45-42Z_INITIAL_TASK.md` — superseded by this file.

## Repository state (at capture)

- **Research phase:** COMPLETE. Experiments E001–E051 recorded in `ledger/RESEARCH_LEDGER.md`; no new research performed in this session. Ledger tail confirms closure through E469 (2026-11-17T22:43:41Z); last substantive entry E051 (Post-Closure Conformance Pass, 2026-11-02). All subsequent ledger entries (E052–E469) are durable-handoff refreshes only.
- **Working tree:** source-clean. `git status` shows only 14 modified tracked `__pycache__/*.pyc` bytecode files under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/` (build artifacts, not source — do not commit). No material changes in `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, or ledger sources. `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/` → only the 14 pyc files.
- **Golden baseline:** 138 tracked artifacts under `experiments/`, all matching HEAD. No `.verify_snapshot/` and no `.verify_reports/` present; no interrupted verification run indicated; nothing to recover.
- **Dependencies:** confirmed importable in system Python 3.12 — numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0, yfinance 1.7.0 (installed this session; a fresh agent session should re-confirm before running any driver).
- **Symlink tree:** 524 total symlinks across root, `handoff/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`, `HANDOFFS/`. All generic canonical pointers resolve to `handoff_2026-11-17T22-45-42Z_INITIAL_TASK.md` (the prior handoff) pending repoint to this file.

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
2. **Repoint canonical aliases:** `python3 scripts/repoint_handoff.py handoff_2026-11-17T22-58-23Z_INITIAL_TASK.md` (mirrors the file to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` and repoints all generic symlinks; verified 0 bad).
3. **Integrity check (before new work):** run `SEED=42 bash scripts/check.sh` (or `make check`). If a golden/baseline mismatch is reported, restore per `AGENTS.md` before proceeding. Escalate to `SEED=42 python3 run_all_verification.py` / `--extended` only if required.
4. **Handle user requests:** follow project conventions (pre-registration, no goalpost changes, no committing verification output, no golden/data re-pins without deliberate update flow). Research program is closed per ledger (E001–E051); avoid speculative new strategy exploration unless explicitly directed and properly pre-registered.
5. **Session close-out (if material work is done):** create a new timestamped durable handoff, repoint canonical handoff aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`, update `ledger/RESEARCH_LEDGER.md` only if appropriate, and do not commit `__pycache__` artifacts.

_No pending implementation tasks carried forward from this handoff._