# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-17T23:29:49Z
**HEAD:** `6d3cae19` (main) "chore(kilo): checkpoint agent session"
**Branch:** main
**Prior handoff:** `handoff_2026-11-17T22-58-23Z_INITIAL_TASK.md` — superseded by this file.

## Repository state (at capture)

- **Research phase:** COMPLETE (E001–E043 per AGENTS.md; surviving strategies in `ledger/RESEARCH_LEDGER.md`). No new research performed this session.
- **Working tree:** source-clean aside from regenerated `__pycache__/*.pyc` build artifacts (do not commit). No material changes in `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, ledger sources.
- **Golden baseline:** `experiments/*.json` match HEAD. No `.verify_snapshot/` and no `.verify_reports/` present; no interrupted verification run to recover.
- **Dependencies:** numpy, pandas, scipy, pyarrow, statsmodels, yfinance importable in system Python 3.12. Re-confirm before running any driver.
- **Symlink tree:** root, `handoff/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`, `HANDOFFS/` canonical pointers resolve to the prior handoff pending repoint to this file.

## Canonical invariants (do not violate)

- `experiments/*.json` are golden artifacts; verification overwrites then restores them — **never leave a run half-finished**.
- On interrupt or golden mismatch: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD holds the pinned baseline).
- Re-pin baselines only via documented `--update` flows (`check_golden_baseline.py`, `check_data_coverage.py`), never as a side effect of verification.
- Always use `SEED=42` for verification/reproduction commands.
- Do not commit `__pycache__/*.pyc` artifacts or verification output.
- Do not modify `.github/workflows/` via automation; template at `.github/workflow-templates/verification-gate.yml`.

## Known open items (from ledger; not blockers)

- E049/E050: E041/E042 grid artifacts remain 1-ulpsensitive under the ill-conditioned tangency QP. Do **not** re-pin to silence drift.
- E048: data-cache coverage is enforced; `scripts/check_data_coverage.py` guards every `data.download()` call site.
- E041 has 133 numeric diffs in extended comparison (ledger E049); most other extended drivers reproduce with 0 diffs.

## Recommended next actions

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` clean aside from `__pycache__/*.pyc` noise and no `.verify_snapshot/`.
2. **Repoint canonical aliases:** `python3 scripts/repoint_handoff.py handoff_2026-11-17T23-29-49Z_INITIAL_TASK.md` (mirrors to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` and repoints generic symlinks).
3. **Integrity check (before new work):** `SEED=42 bash scripts/check.sh` (or `make check`). Restore per `AGENTS.md` before proceeding on any mismatch.
4. **Handle user requests:** follow conventions (pre-registration, no goalpost changes, no committing verification output, no deliberate-repin-only re-pins). Research program closed per ledger — avoid speculative strategy exploration unless explicitly directed and pre-registered.
5. **Session close-out:** if material work is done, create a new timestamped durable handoff, repoint aliases via `python3 scripts/repoint_handoff.py <new_file>`, update `ledger/RESEARCH_LEDGER.md` only if appropriate, and do not commit `__pycache__` artifacts.

_No pending implementation tasks carried forward from this handoff._
