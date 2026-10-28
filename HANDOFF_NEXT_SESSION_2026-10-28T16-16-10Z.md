# HANDOFF — Timestamped clear initial task for next agentic session

Timestamp (UTC): 2026-10-28T16:16:10Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: c4d4643 (chore(kilo): checkpoint agent session)
Working tree: clean except tracked __pycache__/*.pyc files (no canonical artifacts changed)
Verify snapshot: **ACTIVE** — quick verification suite is running (pid 14924, started 2026-10-28T16:19Z). Do NOT interrupt it. If this session ends while it runs, the next session must NOT start another run; instead wait for it or recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Mission for next session
This repo is in post-research state (E001–E043 complete). Surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. Baseline/verification guards are strict: never leave a verification run half-finished, never re-pin goldens as a side effect of verification. No new research is warranted unless explicitly requested. Start by confirming baseline integrity before making any changes.

## Current known state
- Research complete; canonical artifacts are `experiments/*.json`, pinned by `ledger/golden_baseline.json`.
- Data coverage invariant enforced by `scripts/check_data_coverage.py` against `ledger/data_baseline.json` (35 pinned inputs); pinned vintages in `data/vintages.json` (2026-10-12 primary, 2026-10-11 committed), E029 fundamentals pinned in `data/fundamentals/`.
- Optimizer determinism rule pinned by `tests/test_portfolio_opt.py`; `src/portfolio_opt.py` validates on constraints, never solver exit status.
- Verification driver: `run_all_verification.py` (`--quick` / `--extended` / `--full` / `--skip-slow` / `--restore-only`). Always `SEED=42`.
- CI workflow cannot be created by agents. Local equivalents: `make check`, `make verify`, `make verify-quick`, `make verify-extended`, `make verify-full`. Template at `.github/workflow-templates/verification-gate.yml`.

## What was done this session
1. Installed pinned dependencies (`pip install -r requirements.txt`) — the environment was bare (no pandas/numpy/scipy). This was required before any check could run. Dependencies now match `requirements.txt` (numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0, yfinance 1.7.0).
2. Ran `SEED=42 bash scripts/check.sh` — **ALL CHECKS PASSED** (convention robustness, golden guards, data coverage, test_portfolio_opt, experiment imports, template validation). Note: `check_data_coverage.py` alone prints "ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED"; the earlier failures were purely from the missing pandas import, not from the repo state.
3. Started the quick verification suite (`SEED=42 python3 run_all_verification.py`) in the background. It was still running at 16:26Z.

## Immediate priorities (do in order)
1. **Do not start a new verification run while the active one owns `.verify_snapshot/`**. Check `cat .verify_snapshot/ACTIVE.json` for the pid. If the process is gone and the snapshot remains, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
2. **Confirm the running suite finished cleanly** and that `experiments/` is restored to HEAD (only `__pycache__/*.pyc` should show as modified in `git status --short`).
3. **Sanity check** — `SEED=42 bash scripts/check.sh` (all must pass).
4. **Verify reproducibility** — Quick already in progress; Extended: `--extended` (reports E041 drift, do not re-pin).
5. **Recovery if interrupted** — `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. The suite self-recovers at startup and refuses to start while another live run owns `.verify_snapshot/`.

## Known open items
- **E041 numeric drift (~133 diffs)**: 1-ulp sensitivity of the ill-conditioned tangency QP in `src/portfolio_opt.py`. Do NOT re-pin to silence. Root cause already fixed (E049); remaining drift is inherent to the problem.
- **E030 / E029**: offline-reproducible since 2026-10-20 via committed/pinned inputs (ETF panel + fundamentals snapshot).
- **Ledger E048 vs E049**: E048 says E042-lead is unfixed and breaks the primary gate; E049 says it is fixed. Read both before deciding. Authoritative check is `run_all_verification.py` itself.
- **__pycache__ .pyc files are tracked** and show as modified on a clean checkout. Not a baseline concern; do not commit them unless intentionally regenerated.
- **Environment**: dependencies are now installed in the user site (`/home/runner/work/_temp/kilo-home/.local`). A fresh session may need `pip install -r requirements.txt` again if the environment is reset.

## Suggested first command
```bash
cat .verify_snapshot/ACTIVE.json 2>/dev/null; echo "---"; SEED=42 bash scripts/check.sh
```

## Current handoff pointer
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-28T16-16-10Z.md` (see also `HANDOFF_CURRENT.md` and `HANDOFF_NEXT.md`).