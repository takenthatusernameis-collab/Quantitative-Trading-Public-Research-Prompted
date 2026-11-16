# Agentic Work Session Handoff

**Timestamp**: 2026-11-16T11:46:21Z (UTC)
**Project**: Quantitative-Trading-Public-Research-Prompted
**Branch**: `main`
**Session state at handoff**: No active implementation task in progress; baseline integrity re-verified.
**Supersedes**: `handoff/handoff_2026-11-16T11-45-25Z_INITIAL_TASK.md`

---

## INITIAL TASK MESSAGE (for the next agentic work session)

**Primary task:** Maintain baseline integrity and reproducibility. Do not start new research/experiments unless explicitly requested.

1. Read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md` (as needed), and this handoff.
2. Check coordination context (`board_read`) for any pending coordinator/peer task before acting.
3. Run fast integrity check: `SEED=42 bash scripts/check.sh` (or `make check`). Fix any failures before other work.
4. If deeper verification is requested, use `SEED=42 python3 run_all_verification.py` (`--extended`/`--full` as needed). **Never leave a verification run half-finished.**
5. If you find `.verify_snapshot/`, stale golden diffs, or interrupted verification output, recover first: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`/`ledger/golden_baseline.json` rules).

**If no task is posted:** remain in maintenance mode (integrity checks, documentation hygiene consistent with conventions). Research phase is complete (E001–E043); follow pre-registration, promotion-gate, and negative-result recording conventions for any new work.

---

## Project Status

- **Research phase**: Complete (E001–E043). Validated findings in `ledger/RESEARCH_LEDGER.md`.
- **Canonical baseline**: `experiments/*.json` goldens; pinned hashes in `ledger/golden_baseline.json`.
- **CI**: Workflow template only (`.github/workflow-templates/verification-gate.yml`); maintainer must create actual workflow via GitHub UI.

## Verified at handoff

- `SEED=42 bash scripts/check.sh` → **ALL checks passed** (exit 0, 2026-11-16T11:46Z), including `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `check_json_artifacts.py`, portfolio-opt determinism tests, and all experiment-driver import/call checks.
- No `.verify_snapshot/` directory present (no interrupted verification run).
- `git status --short`: only modified `__pycache__/*.pyc` build artifacts (15 files); no tracked `experiments/` or source changes in flight.
- Recent commits: `2f17dd55`, `c6c1cca8`, `c49a9deb`, `8d0b65d4`, `2c537f04` (`chore(kilo): checkpoint agent session`).

## Key constraints / reminders

- **Always `SEED=42`** for verification/repro runs. Primary convention: close-to-close v1.2.3.
- **Never commit verification output/captured goldens** as a side effect of a run; if interrupted, restore before committing.
- **Do not re-pin** E041/E042 grid artifacts to silence known ill-conditioned QP 1-ulp drift (ledger E049 open item).
- Cache/data coverage is enforced (`QUANT_RESEARCH_OFFLINE=1` in verification; pinned vintages/snapshots per `data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`).
- **Symlink note**: several top-level durable pointers (`INITIAL_TASK.md`, `LATEST.md`, `NEXT.md`, `handoff.md`, `handoff_CURRENT.md`) currently resolve to a missing target `handoff_2026-11-16T11-45-25Z_INITIAL_TASK.md` at repo root. The real files live under `handoff/`. This handoff corrects the pointers to the `handoff/`-prefixed target.

## Useful commands

```bash
SEED=42 bash scripts/check.sh          # fast offline gate
make verify-quick                      # ~8 min
make verify-extended                   # ~21 min
make verify-full                       # ~15 min
SEED=42 python3 run_all_verification.py --restore-only
```

*Durable handoff for next agentic session. Update if material state changes.*