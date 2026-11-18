# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-18T04-43-04Z
**HEAD:** `c7f78ff3286cb80c5e47ae30d3f22c429629f3d8` (main, 2026-11-18 04:42:57 +0000) `chore(kilo): checkpoint agent session`
**Branch:** `main` (in sync with `origin/main`; 0 ahead / 0 behind)
**Supersedes:** `handoff_2026-11-18T04-42-45Z_INITIAL_TASK.md`

## Repository state (at capture)

- **Research phase:** COMPLETE. Experiments E001–E051 are recorded in `ledger/RESEARCH_LEDGER.md`; all later ledger entries (E052+) are durable-handoff refreshes / conformance audits only. No new research is in progress.
- **Working tree:** source-clean except 12 modified tracked `__pycache__/*.pyc` files under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/` (build artifacts). Do **not** stage or commit them.
- **Golden artifacts:** 107 JSON artifacts under `experiments/`; `git diff --name-only HEAD -- experiments/` is empty (no golden drift at capture). All 107 match `ledger/golden_baseline.json` and HEAD.
- **Verification state:** no `.verify_snapshot/` and no `.verify_reports/` present; no interrupted verification run to recover.
- **Preceding commit note:** `c7f78ff3` repointed the generic handoff aliases to `handoff_2026-11-18T04-42-45Z_INITIAL_TASK.md` (the prior refresh target); it did **not** change the handoff content itself. This refresh supersedes that target with a fresh timestamped artifact.

## Environment caveat (carry forward)

- `python3` (3.12.3) on this runner lacks `pandas`/`numpy`/`scipy`/`pyarrow`/`statsmodels`/`yfinance` (confirmed: `import pandas` raises `ModuleNotFoundError`). `scripts/check.sh` therefore stops at the pandas-dependent unittest steps.
- Fix before running the full gate: `python3 -m pip install -r requirements.txt`.
- Non-pandas checks that do run cleanly here: `scripts/check_json_artifacts.py`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py` (all expected to pass on a clean baseline).

## Canonical invariants (do not violate)

- Treat `experiments/*.json` as canonical goldens. Verification overwrites them during runs and restores afterward — never leave a run half-finished.
- If interrupted or on golden/baseline mismatch: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD still holds the pinned baseline). See `AGENTS.md` "Baseline Integrity".
- Re-pin `experiments/` or `data/` baselines only via explicit documented `--update` flows (`python3 scripts/check_golden_baseline.py --update`, `python3 scripts/check_data_coverage.py --update`); never as a side effect of verification.
- Always use `SEED=42` for verification/reproduction. Do not commit `__pycache__` artifacts or verification output.
- Generic handoff aliases must resolve to the latest durable timestamped handoff; preserve historical timestamped/special handoff files. Repoint with `python3 scripts/repoint_handoff.py <new_handoff_file>`.

## Known open items (from ledger/AGENTS; not blockers)

- **E049/E050:** E041/E042 grid artifacts remain 1-ulp sensitive under the ill-conditioned tangency QP (optimizer constraint-validation defect fixed; exact KKT enumeration routes the QP per E050). Numeric drift remains in the extended comparison — do **not** re-pin to silence it.
- **E048:** data-cache coverage is an enforced invariant (`scripts/check_data_coverage.py` / `ledger/data_baseline.json`); add inputs only by committing files and re-pinning via `--update`.
- CI verification workflow cannot be pushed by automated agents; a maintainer must create it from `.github/workflow-templates/verification-gate.yml` (see `VERIFICATION_GATE_TEMPLATE.md`).

## Initial task for next session

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` shows only expected `__pycache__/*.pyc` noise and no `.verify_snapshot/`.
2. **Integrity gate before changes:** `python3 -m pip install -r requirements.txt` (if deps missing), then `SEED=42 bash scripts/check.sh` (or `make check`). If golden/baseline/data issues are reported, restore/fix per `AGENTS.md` before proceeding. Escalate to `SEED=42 python3 run_all_verification.py` / `--extended` only when warranted.
3. **Handle user-directed work:** follow project conventions (pre-registration, no goalpost changes, no committing verification output, no golden/data re-pins without deliberate update flow). Research program is closed (E001–E051); avoid speculative new strategy exploration unless explicitly requested and properly pre-registered.
4. **Close-out (if material work performed):** create a new timestamped durable handoff, repoint canonical aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`, mirror it identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`, update `ledger/RESEARCH_LEDGER.md` only if appropriate, and leave no `__pycache__`/verification artifacts staged.

_No pending implementation tasks carried forward from this handoff._

(End of file - total 43 lines)
