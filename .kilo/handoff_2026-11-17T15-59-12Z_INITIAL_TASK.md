# Durable Handoff — Initial Task Message (next agentic work session)

**Created:** 2026-11-17T15:59:12Z (UTC)
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Handoff file:** `handoff_2026-11-17T15-59-12Z_INITIAL_TASK.md`

## 1) Snapshot of state at handoff

- **HEAD:** `ce076bc705642cc91dbb19d939b92cc5949d520d` (`chore(kilo): checkpoint agent session`) on `main`.
- **Sync:** `git rev-parse origin/main` == HEAD; `git rev-list --left-right --count origin/main...HEAD` → `0 0` (in sync with origin).
- **Working tree:** only tracked `__pycache__/*.pyc` build artifacts modified under `scripts/`, `src/`, `tests/` (gitignored bytecode). No source, driver, experiment artifact, data, test, or `research_state/` changes are uncommitted. `experiments/` and `data/` are clean relative to HEAD.
- **Integrity sentinels:** no `.verify_snapshot/` and no `.verify_reports/` present → no interrupted verification run to recover.
- **Research status:** repository is **closed**. Research phase E001–E051 complete; `experiments/*.json` are committed golden artifacts (107 pinned in `ledger/golden_baseline.json`). Durable-handoff bookkeeping continues in `ledger/RESEARCH_LEDGER.md` (last recorded prior to this refresh: E462 at 2026-11-17T15:55:27Z, HEAD `ce076bc7`).
- **Prior handoff superseded:** `handoff_2026-11-17T15-58-10Z_INITIAL_TASK.md` (and its generic alias targets) is read/retained for history; this refresh supersedes it operationally.
- **Delta vs prior durable handoff:** checkpoint/handoff bookkeeping only. No changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/` sources. Prior research state adopted unchanged.

## 2) Verification status

- **This session:** integrity/state inspection only (HEAD/sync/cleanliness of `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`; absence of `.verify_snapshot/`/`.verify_reports/`). No verification suite was executed to avoid unnecessary churn and to avoid touching golden artifacts.
- **Last recorded full guard pass:** E462 recorded `SEED=42 bash scripts/check.sh` → `=== All checks passed ===` and `python3 scripts/check_golden_baseline.py` → all 107 pinned golden artifacts matched at HEAD `ce076bc7`; subsequent deltas are checkpoint/bookkeeping only (no source/artifact/data changes), so that result is expected to still hold. **Reconfirm before any substantive work.**

## 3) Clear initial task for the next agentic session

**Default: no new research is requested; the research phase is closed.** Do not start new experiments unless explicitly authorized by the user and pre-registered per `AGENTS.md` / `ledger/PRIORITIZATION.md`.

1. **Confirm state (read-only):**
   - `git status --short` — expect only `__pycache__/*.pyc` modifications.
   - `git rev-parse HEAD && git rev-parse origin/main && git rev-list --left-right --count origin/main...HEAD` — expect `ce076bc7...` / in sync (`0 0`) or explain any drift.
   - Confirm no `.verify_snapshot/` or `.verify_reports/` exist; confirm `experiments/` and `data/` clean vs HEAD.
2. **Run fast integrity checks:** `SEED=42 bash scripts/check.sh` (or `make check`). If it reports a golden mismatch, **stop and fix before committing** — do not re-pin as a side effect of verification.
3. **If deeper verification is warranted:** `SEED=42 python3 run_all_verification.py` (quick, ~8 min), or `--extended` / `--full` per `AGENTS.md`. Never leave a run half-finished. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `ledger/golden_baseline.json` if HEAD already contains a captured run).
4. **If you make any substantive change:** record outcome as the next ledger entry (E463+) in `ledger/RESEARCH_LEDGER.md` with live HEAD, UTC timestamp, actions, result, and constraints honored. Follow all pre-registration/multiple-testing rules for any new research.
5. **Commit/push policy:** do **not** commit or push unless explicitly directed by the user. Do not commit `__pycache__` artifacts.

## 4) Standing constraints & known open items (must read)

- **Canonical artifacts:** `experiments/*.json` are committed goldens; suite overwrites then restores them. Never leave half-finished. Backup/marker lives in gitignored `.verify_snapshot/`.
- **Golden guards (first-class):** `scripts/check_goldens_clean.py` (working tree vs HEAD) and `scripts/check_golden_baseline.py` (SHA-256 vs `ledger/golden_baseline.json`) run in `scripts/check.sh` and the suite. Re-pin only deliberately with `python3 scripts/check_golden_baseline.py --update` and only when intentionally replacing a baseline (never to silence a verification run).
- **Data coverage invariant:** every `data.download()` call site must resolve to a git-tracked, SHA-256-pinned cache file per `ledger/data_baseline.json` (`scripts/check_data_coverage.py`). Suite runs drivers with `QUANT_RESEARCH_OFFLINE=1`.
- **Reproducibility:** always `SEED=42`. Close-to-close is the v1.2.3 primary convention; overnight decomposition reported alongside.
- **Known benign drift (do NOT re-pin):** tangency QP (`src/portfolio_opt.py` `max_sharpe` / `min_var`) remains ill-conditioned; 1-ulp sensitivity can move E041/E042 grid artifacts by ~1e-05, so `--extended` may still report E041 (and sometimes E042 grid) drifting by 29–133 numeric differences. This is a documented research-engineering decision (ledger E049 open item + E050), not a defect to re-pin away. Optimizer answers must be judged on the **problem's constraints**, not solver exit status (pinned by `tests/test_portfolio_opt.py`).
- **Handoff mechanism:** durable files are `handoff_<UTC>_INITIAL_TASK.md` at repo root, mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`; generic canonical aliases are repointed via `python3 scripts/repoint_handoff.py handoff_<UTC>_INITIAL_TASK.md`. Timestamped/historical aliases must remain untouched.

## 5) Quick commands

```bash
# State & integrity (fast, offline)
git status --short
SEED=42 bash scripts/check.sh          # or: make check

# Verification tiers
SEED=42 python3 run_all_verification.py              # quick ~8 min
SEED=42 python3 run_all_verification.py --extended   # ~21 min
SEED=42 python3 run_all_verification.py --full       # ~15 min (heavier E042/grid)

# Recovery if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

*End of durable handoff. Retain for history; supersede only with a newer timestamped durable handoff that is fully mirrored and repointed.*
