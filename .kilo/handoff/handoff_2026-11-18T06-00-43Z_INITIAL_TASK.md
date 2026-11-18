# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-18T06-00-43Z
**HEAD:** `047fb2e33c43d373be8dcc708214d05e3eba2721` (main, 2026-11-18T06:00:06Z)
**Branch:** `main` (in sync with `origin/main`; 0 ahead / 0 behind)
**Supersedes:** `handoff_2026-11-18T05-59-54Z_INITIAL_TASK.md` (most recent timestamped artifact; this refresh is mirrored to the canonical handoff directories and repointed)

## 1) First action (do this immediately)

Run the fast integrity gate and confirm a clean baseline before making changes:

```bash
SEED=42 make check
# or, without make: SEED=42 bash scripts/check.sh
```

If `make check` fails due to golden / data-coverage / baseline drift, stop and resolve that first (do not paper over by re-running verification blindly). See `AGENTS.md` section "Baseline Integrity".

## 2) Repository state (at capture)

- **Research phase:** COMPLETE. Experiments E001–E051 are recorded in `ledger/RESEARCH_LEDGER.md`; later ledger entries (through E484) are durable-handoff refreshes / conformance audits only. No new research is in progress.
- **Working tree:** source-clean except tracked `__pycache__/*.pyc` build artifacts under `scripts/__pycache__/`, `src/__pycache__/`, and `tests/__pycache__/`. Do **not** stage or commit them.
- **Golden artifacts:** 107 JSON artifacts under `experiments/`; `git diff --name-only HEAD -- experiments/` is empty — all match HEAD and `ledger/golden_baseline.json`.
- **Verification state:** no `.verify_snapshot/` and no `.verify_reports/` present; no interrupted verification run to recover.
- **Handoff hygiene:** this handoff is written at repo root and mirrored byte-identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, and `.kilo/handoff/`; generic canonical aliases are repointed via `scripts/repoint_handoff.py`.

## 3) Environment note (carry forward)

- This session: `python3` (3.12.x) imports the full core stack cleanly — `pandas`, `numpy`, `scipy`, `pyarrow`, `statsmodels`, `yfinance` all import OK. So `scripts/check.sh` should be able to run its pandas-dependent steps here.
- If a future runner reports `ModuleNotFoundError` (e.g. `No module named 'pandas'`), fix first with: `python3 -m pip install -r requirements.txt`.
- Non-pandas checks that always run cleanly on a clean baseline: `scripts/check_json_artifacts.py`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.

## 4) Common verification entry points

```bash
SEED=42 make verify-quick        # ~8 min
SEED=42 make verify-extended     # ~21 min
SEED=42 make verify-full         # ~15 min
```

If interrupted, recover goldens:

```bash
SEED=42 python3 run_all_verification.py --restore-only
# or, only when HEAD still holds the pinned baseline: git checkout -- experiments/
```

## 5) Canonical invariants (do not violate)

- Treat `experiments/*.json` as canonical goldens. Verification overwrites them during runs and restores afterward — never leave a run half-finished.
- Re-pin `experiments/` or `data/` baselines only via the explicit documented `--update` flows (`python3 scripts/check_golden_baseline.py --update`, `python3 scripts/check_data_coverage.py --update`); never as a side effect of verification.
- Always use `SEED=42` for verification/reproduction. Do not commit `__pycache__` artifacts or verification output.
- Generic handoff aliases must resolve to the latest durable timestamped handoff; preserve historical timestamped/special handoff files. Repoint with `python3 scripts/repoint_handoff.py <new_handoff_file>`.

## 6) Known open items (from ledger/AGENTS; not blockers)

- **E049/E050:** E041/E042 grid artifacts remain 1-ulp sensitive under the ill-conditioned tangency QP (optimizer constraint-validation defect fixed; exact KKT enumeration routes the QP per E050). Numeric drift remains in extended comparison — do **not** re-pin to silence it.
- **E048:** data-cache coverage is an enforced invariant (`scripts/check_data_coverage.py` / `ledger/data_baseline.json`); add inputs only by committing files and re-pinning via `--update`.
- **CI:** the verification workflow cannot be pushed by automated agents; a maintainer must create it from `.github/workflow-templates/verification-gate.yml` (see `VERIFICATION_GATE_TEMPLATE.md`).

## 7) Initial task for next session

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` shows only expected tracked `__pycache__/*.pyc` noise and no `.verify_snapshot/`.
2. **Integrity gate before changes:** (deps present this session; otherwise `python3 -m pip install -r requirements.txt`) then `SEED=42 bash scripts/check.sh` (or `make check`). If golden/baseline/data issues are reported, restore/fix per `AGENTS.md` before proceeding. Escalate to `run_all_verification.py` / `--extended` only when warranted.
3. **Handle user-directed work:** follow project conventions (pre-registration, no goalpost changes, no committing verification output, no golden/data re-pins without the deliberate update flow). Research program is closed (E001–E051); avoid speculative new strategy exploration unless explicitly requested and properly pre-registered.
4. **Close-out (if material work performed):** create a new timestamped durable handoff, mirror it identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`, repoint canonical aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`, add a ledger entry if appropriate, and leave no `__pycache__`/verification artifacts staged.

_No pending implementation tasks carried forward from this handoff._