# Agentic Handoff — Initial Task (Next Work Session)

**Timestamp (UTC):** 2026-11-17T23:31:34Z
**Workspace:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `0548bc95` (`main`) — `chore(kilo): checkpoint agent session`
**Supersedes:** `handoff_2026-11-17T23-29-49Z_INITIAL_TASK.md`

## Repository state

- **Research phase:** Complete (E001–E043). Surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. No new research started this session.
- **Working tree:** Clean aside from modified `__pycache__/*.pyc` files in `scripts/`, `src/`, and `tests/` (build artifacts; do not commit). No material changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or ledger sources.
- **Golden baseline:** `experiments/*.json` are the canonical artifacts. No `.verify_snapshot/` or `.verify_reports/` present; no interrupted verification run to recover.
- **Environment:** Python 3.12 with core dependencies (numpy, pandas, scipy, pyarrow, statsmodels, yfinance) available. Re-confirm before driver runs if needed.

## Invariants (do not violate)

- `experiments/*.json` are goldens; verification overwrites then restores them — **never leave a run half-finished**.
- If a run is interrupted or goldens mismatch: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD holds the pinned baseline). Follow `AGENTS.md` “Baseline Integrity”.
- Always use `SEED=42` for verification/reproduction. Do not commit verification output or `__pycache__` artifacts.
- Re-pin baselines only via documented `--update` flows (`check_golden_baseline.py`, `check_data_coverage.py`), never as a side effect of verification.
- Do not modify `.github/workflows/` via automation (template: `.github/workflow-templates/verification-gate.yml`).

## Known open items (ledger context, not blockers)

- E049/E050: E041/E042 tangency-grid artifacts remain 1-ulp sensitive; do **not** re-pin to silence drift.
- E048: data-cache coverage enforced via `scripts/check_data_coverage.py` / `ledger/data_baseline.json`.

## Initial task for the next agentic session

1. **Orient:** Read this handoff and `AGENTS.md`. Confirm `git status` is clean aside from `__pycache__/*.pyc` and no `.verify_snapshot/` exists.
2. **Smoke/integrity check (recommended first action):**
   ```bash
   SEED=42 bash scripts/check.sh
   # or: make check
   ```
   If it fails, diagnose per `AGENTS.md` and restore state before proceeding (`--restore-only` if a verification snapshot is involved).
3. **Handle user requests:** Follow project conventions (pre-registration, no goalpost changes, multiple-testing discipline, honest negative results). The research program is closed per ledger—avoid speculative new strategy exploration unless explicitly directed and properly pre-registered.
4. **Session close-out (if you make material changes):** Run relevant checks, create a new timestamped durable handoff, repoint aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`, and do not commit `__pycache__` or verification output unless explicitly requested.

_No pending implementation tasks carried forward._
