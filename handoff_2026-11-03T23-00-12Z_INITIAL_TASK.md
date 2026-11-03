# INITIAL TASK HANDOFF

**Timestamp:** 2026-11-03T23:00:12Z
**From:** Current agentic work session
**To:** Next agentic work session
**Repository:** Quantitative-Trading-Public-Research-Prompted
**HEAD:** `2759ea9` "chore(kilo): checkpoint agent session" (matches `origin/main`, no local-ahead commits)

---

## Context

This repository contains independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.

- **Research phase:** Complete (E001–E043)
- **Surviving validated strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden artifacts:** `experiments/*.json` (138 committed) are the canonical research artifacts, protected by `ledger/golden_baseline.json`. The verification suite backs them up and restores them — they must never be left modified.

## Repo State (verified at handoff time)

- Working tree **clean** except for `__pycache__/*.pyc` bytecode drift (binary-only, no source changes). `git status --short` filtered for non-pycache = empty.
- `git fetch origin main` succeeded; `HEAD` = `origin/main` = `refs/heads/main` = `2759ea9`. Zero local-ahead commits, no divergence.
- `.verify_snapshot/` **ABSENT** — no live verification run, nothing to recover.
- No stash.

## Primary Goal

Verify repository integrity and confirm the baseline is clean before starting any new work. Follow all conventions in `AGENTS.md`.

## Recommended Initial Tasks (In Order)

### 1) Verify Baseline Integrity
```bash
SEED=42 bash scripts/check.sh
# or
make check
```
Runs `py_compile`, `check_goldens_clean.py` (working tree vs HEAD), `check_golden_baseline.py` (tracked artifacts vs `ledger/golden_baseline.json` SHA-256 pins), `check_data_coverage.py` (all `data.download()` inputs pinned and git-tracked), and the test suite. Must pass green before any commit.

### 2) If Clean, Run Quick Verification (Optional but Recommended)
```bash
SEED=42 python3 run_all_verification.py
# or
make verify-quick
```
(~8 min). Re-runs the 8 drivers in the quick block (E012, E023, E024-merge, E027, E035, E037, E039, E042-lead) and restores goldens afterwards.

### 3) Review Research State
- Read `ledger/RESEARCH_LEDGER.md` for current status of experiments and open items.
- Review `ledger/golden_baseline.json` to understand the pinned baseline.
- Check `.verify_snapshot/` — if a stale snapshot exists with no live run, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## If `check.sh` Reports a Golden Mismatch

Fix it **before** committing. Do **not** let a verification run capture output into `experiments/`. If a run was interrupted and `experiments/` holds driver output instead of goldens, restore first:

```bash
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

Then re-pin only through `python3 scripts/check_golden_baseline.py --update` (puts the replacement in the diff) — never as a side effect of running the suite.

## Key Conventions to Honor

- Always run with `SEED=42`.
- `QUANT_RESEARCH_OFFLINE=1` is used by the suite; missing cache entries fail hard.
- Never modify `experiments/*.json` as a side effect of verification — the suite handles backup/restore.
- Never commit secrets/keys; never add comments to code unless asked.
- Do not commit unless explicitly requested.
- New `data.download()` input requires a committed cache file + `ledger/data_baseline.json` re-pin via `python3 scripts/check_data_coverage.py --update`.

## Known Invariants / Caveats

- E029, E030 offline-reproducible since 2026-10-20 (data pinned in `data/fundamentals/` and committed panel).
- E041 has remaining numeric drift (1-ulp sensitivity of ill-conditioned QP, 133 diffs) — DO NOT re-pin.
- E042 lead artifact likewise drifts — DO NOT re-pin.
- Optimizer (`src/portfolio_opt.py`) validates on the problem's constraints, never on solver exit status; pinned by `tests/test_portfolio_opt.py`.
- Close-to-close is the v1.2.3 primary convention; overnight decomposition reported alongside.
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance); cvxpy/cvxopt optional.
- Repro caveat (`HANDOFF_REPRO_CAVEAT.md`): E041/E042 sensitivity grids are not byte-exact in this sandbox; no gate/decision affected.
- CI verification-gate workflow template: `.github/workflow-templates/verification-gate.yml`; a maintainer must create the actual workflow via GitHub UI (agents cannot).

## Quick Commands

```bash
ls -la .verify_snapshot/ 2>&1 | head
git status --short && git rev-parse HEAD origin/main
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --full   # ~15 min full verification
```

---

**Ready to proceed. Start with step 1 (baseline integrity check). Wait for explicit user instructions before taking any research action.**