# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-19T18-13-00Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `db56bccd` ("chore(kilo): checkpoint agent session") — `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Supersedes as the current durable artifact:** `handoff_2026-11-19T18-12-26Z_INITIAL_TASK.md`
(earlier handoffs are retained unchanged for history)

## Start here (ordered — do this first)

1. **Orient on the live state.**
   `git rev-parse HEAD && git status --short --branch`
   Confirm you are on `main` at `db56bccd` (or a later checkpoint, still tracking
   `origin/main`). Ignore gitignored `__pycache__/*.pyc` churn and `research_state/`
   runtime diagnostics; anything else modified under `experiments/`, `ledger/`, `data/`,
   `src/`, or `tests/` needs an explanation before you proceed.

2. **Recover any interrupted verification.** Check `.verify_snapshot/`. If it exists
   (a previous run was killed / OOM / timed out), restore the canonical baseline
   **before** any other work:
   `SEED=42 python3 run_all_verification.py --restore-only`
   Never leave a verification run half-finished — it overwrites `experiments/*.json`.

3. **Confirm both golden guards pass.** Cheap, and both must be green:
   `python3 scripts/check_goldens_clean.py`   → "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD"
   `python3 scripts/check_golden_baseline.py` → "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT"
   A failure means the baseline is dirty: restore the pinned artifact **before** committing.

4. **Provision the environment — it is NOT preinstalled on this runner.**
   `python3 -c "import numpy"` currently fails with `ModuleNotFoundError: No module named 'numpy'`.
   Run `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels,
   yfinance) before any Python-dependent step. `cvxpy`/`cvxopt` are optional (the
   optimizer falls back to `scipy.optimize`).

5. **Run the fast gate.** `SEED=42 bash scripts/check.sh` (or `make check`). Offline,
   seconds; exercises convention checks, golden guards, data-coverage invariant, and the
   portfolio-optimizer determinism test.

6. **Then: await explicit instructions.** Research phase is complete. Do not invent new
   experiments, re-run verification unprompted, move pre-registered gates, or touch
   baseline artifacts without explicit direction.

7. **When done, leave your own timestamped handoff** (see "Recurring handoff procedure").

## Current state (verified at handoff)

- **Research phase:** complete (E001–E537 ledger entries). Authoritative dispositions and
  surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. Entries E5xx are
  durable-handoff refresh records only; no actionable OPEN / PENDING / BLOCKED / TODO
  research items were found.
- **Verification snapshot:** `.verify_snapshot/` absent. `.verify_reports/` absent.
  No interrupted verification run pending recovery.
- **Golden integrity:** both guards ran green at this handoff (exit 0): committed
  `experiments/*.json` match HEAD and all 107 artifacts match the
  `ledger/golden_baseline.json` fingerprint.
- **Working tree:** branch `main...origin/main`, clean apart from gitignored
  `__pycache__/*.pyc` timestamp churn and `research_state/` diagnostics (outside the
  tracked baseline). No uncommitted changes to baselines.
- **Environment:** Python deps **not** importable at handoff time (`numpy` missing);
  step 4 above is required before running scripts.
- **Baselines/artifacts untouched by this session:** `experiments/*.json`,
  `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` and
  `data/fundamentals/` inputs.

## Verification / reproduction scopes (always `SEED=42`)

```bash
SEED=42 bash scripts/check.sh                        # fast guards (offline, seconds)
SEED=42 python3 verify_convention_robustness.py      # read-only convention check
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # ~21 min, 26+ drivers
SEED=42 python3 run_all_verification.py --full       # ~15 min, E042 n_sim=50 + grid
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after a kill
```

The suite backs `experiments/*.json` up to `.verify_snapshot/` and restores them on exit.
A killed run leaves the tree holding driver output instead of goldens — restore before
committing (this has silently replaced the baseline before; see `AGENTS.md`).

## Integrity rules (non-negotiable)

- **Never commit verification output over the canonical goldens.** `experiments/*.json`
  are the authoritative record; the committed golden wins over the latest re-run.
- **Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence
  drift.** Re-pin only on explicit, intentional re-baseline direction with ledger
  justification, via `scripts/check_golden_baseline.py --update`; the re-pin must appear
  in the diff.
- **Known, accepted drift — do not "fix" by re-pinning:** E041/E042 grid artifacts drift
  29–133 numeric diffs (1-ulp sensitivity of an ill-conditioned tangency QP).
  E029/E030 were root-caused and are offline-reproducible from pinned snapshots.
  Closed optimizer-determinism items (E049/E050) stay closed.
- **Offline data invariant:** the verification suite runs with
  `QUANT_RESEARCH_OFFLINE=1`. Every `data.download()` input must be committed and
  SHA-256-pinned in `ledger/data_baseline.json`
  (`python3 scripts/check_data_coverage.py` enforces this). yfinance is not bit-reproducible,
  so an unpinned input is a live download and a repro failure.
- **Optimizer rule (ledger E049):** `src/portfolio_opt.py` validates solver answers on the
  problem's constraints, never on solver exit status. Pinned by `tests/test_portfolio_opt.py`.
- **CI:** do not create `.github/workflows/` gates as an automated agent — the controller
  cleans them and the token lacks `workflows` push. Template lives in
  `.github/workflow-templates/verification-gate.yml`; a maintainer must add it.
- **Pre-registration:** never move gates, sensitivity grids, falsification expectations, or
  recorded outcomes post-hoc without explicit justification and a ledger entry.
- **Secrets:** never commit or log secrets or keys.
- **Commit policy:** do not commit unless explicitly asked.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants.
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items.
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `experiments/*.json` — canonical research artifacts.
- `scripts/check.sh`, `run_all_verification.py`, `scripts/check_data_coverage.py`.
- `scripts/repoint_handoff.py` — repoints stable handoff aliases.

## Recurring handoff procedure (if asked again)

1. Write `handoff_<UTC-TS>_INITIAL_TASK.md` at the repo root (format: `YYYY-MM-DDTHH-MM-SSZ`).
2. Mirror it byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`,
   `.kilo/handoff/` and record one shared SHA-256 (`sha256sum`).
3. Repoint the stable alias symlinks:
   `python3 scripts/repoint_handoff.py handoff_<UTC-TS>_INITIAL_TASK.md`
   It leaves timestamped/historical names untouched and audits every pointer.
4. Append an `E###: Durable Handoff Refresh — Clear Initial Task Message (HEAD <sha>)`
   entry to `ledger/RESEARCH_LEDGER.md` with the SHA-256, guards run, and repoint counts.
5. Do not commit unless explicitly directed.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-19T18-13-00Z_INITIAL_TASK.md`
  (repo root), mirrored to the five handoff directories and linked from the stable aliases
  (`HANDOFF.md`, `LATEST.md`, `INITIAL_TASK.md`, `NEXT_SESSION.md`, etc.).
- **Scope of this session:** handoff artifact + ledger bookkeeping only. No code, experiment,
  ledger disposition, baseline fingerprint, or canonical artifact changed.
- **Next session begins at step 1 above.**

(End of file - total 130 lines)