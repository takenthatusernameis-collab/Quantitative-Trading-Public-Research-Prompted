# Handoff — Initial Task for the Next Agentic Work Session

**Created (UTC):** 2026-11-18T14:36:21Z
**Session type:** Durable handoff refresh (no new research performed)
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Supersedes:** `handoff_2026-11-18T14-35-43Z_INITIAL_TASK.md` (ledger E499)

## START HERE — Initial task for the next agentic work session

1. **Orient (read-only, ~1 min).** Read `AGENTS.md`, this handoff, and the tail of
   `ledger/RESEARCH_LEDGER.md` (entries E497–E499). Then confirm state:
   ```bash
   git status --short
   git rev-parse --short HEAD
   git rev-list --left-right --count HEAD...@{u}
   git diff --name-only HEAD -- experiments/     # must be empty
   ls .verify_snapshot/ACTIVE.json 2>/dev/null   # must not exist
   ```
2. **Fast integrity gate (offline, ~seconds).** Run `SEED=42 bash scripts/check.sh`
   (or `make check`). It validates JSON templates, golden cleanliness
   (`check_goldens_clean.py`), the pinned golden baseline
   (`check_golden_baseline.py`), data-cache coverage
   (`check_data_coverage.py`), and `tests/test_portfolio_opt.py`.
   Fix any baseline/golden/coverage issue **before** any commit.
3. **Install deps if the gate cannot start.** On this bare runner the system
   interpreter is `/usr/bin/python3` 3.12.3 with no core packages
   (`import pandas` → `ModuleNotFoundError`). Fix with
   `python3 -m pip install -r requirements.txt`.
4. **Only if asked to re-verify research**, pick one level and let it finish:
   - `SEED=42 python3 run_all_verification.py` (`make verify-quick`, ~8 min)
   - `SEED=42 python3 run_all_verification.py --extended` (~21 min)
   - `SEED=42 python3 run_all_verification.py --full` (~15 min)
   Never leave a run half-finished: it overwrites `experiments/*.json` mid-run.
   Recover with `SEED=42 python3 run_all_verification.py --restore-only`.
5. **Do not start new research or move goalposts.** Research phase is complete
   (E001–E051 in `ledger/RESEARCH_LEDGER.md`). This handoff is continuity only.
6. **If the user only asks for another handoff refresh**, repeat the convention:
   write `handoff_<UTC ISO>_INITIAL_TASK.md` at repo root, mirror it
   byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`,
   `.kilo/handoff/`, run
   `python3 scripts/repoint_handoff.py handoff_<UTC ISO>_INITIAL_TASK.md`,
   then append the next `E###` entry under the handoff-refresh section of
   `ledger/RESEARCH_LEDGER.md`. Do not commit unless explicitly asked.

## Current state at handoff creation

- Branch: `main` tracking `origin/main`; **0 ahead / 0 behind**.
- `HEAD`: `d387367eb045104165e9a102c2c2d2b492cc0ae1` (`d387367e`).
- `git status --short`: empty (clean working tree).
- `git diff --name-only HEAD -- experiments/`: empty (all goldens match HEAD).
- No `.verify_snapshot/ACTIVE.json` and no `.verify_reports/`: no verification
  run in progress or half-finished.
- Environment: `/usr/bin/python3` 3.12.3; core scientific deps **absent**
  (`pandas`, and therefore numpy/scipy/pyarrow/statsmodels/yfinance). `scripts/check.sh`
  was **not** executed this session; run it first next session after installing deps.

## Key integrity notes (do not violate)

- **Goldens are authoritative.** `experiments/*.json` are the canonical committed
  artifacts. A verification run backs them up (`.verify_snapshot/`, gitignored)
  and restores them. The committed golden, not the latest re-run, is the record.
- **Never re-pin as a side effect.** Replacing a golden or data baseline requires
  `scripts/check_golden_baseline.py --update` /
  `scripts/check_data_coverage.py --update`, which must appear as an explicit diff.
- **Known drift is documented, not a bug.** E041/E042 tangency-QP grid artifacts
  drift by ~29–133 numeric differences from 1-ulp ill-conditioning (ledger E049);
  decisions and gate flags are unchanged. Do **not** re-pin to silence it.
- **Offline reproducibility.** Verification runs with `QUANT_RESEARCH_OFFLINE=1`;
  data inputs are pinned via `data/vintages.json`,
  `data/fundamentals_vintages.json`, and `ledger/data_baseline.json`.
- **Always `SEED=42`.** Close-to-close is the v1.2.3 primary convention; overnight
  decomposition is reported alongside.
- **Do not commit** verification output, re-pinned baselines, `__pycache__`, or
  anything at all unless the user explicitly asks.

## Handoff provenance

- **Durable artifact (this file):** `handoff_2026-11-18T14-36-21Z_INITIAL_TASK.md`
  (repo root), mirrored byte-identically into `handoff/`, `HANDOFFS/`,
  `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- **Canonical pointers:** repointed with
  `python3 scripts/repoint_handoff.py handoff_2026-11-18T14-36-21Z_INITIAL_TASK.md`.
- **Ledger:** recorded as E499 in `ledger/RESEARCH_LEDGER.md`.

_End of durable handoff. No new research requested; awaiting explicit user instructions._
