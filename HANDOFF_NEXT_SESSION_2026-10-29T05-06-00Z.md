# HANDOFF - Next Agentic Work Session
Timestamp (UTC): 2026-10-29T05:06:00Z
Message time: 2026-10-29T05:05:40Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: 18bc5d17f3a25a6216f0d020c8b909fb49eebde2
Working dir: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State (verified this session)
- Research phase complete (E001-E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- All goldens are the committed baselines (`experiments/*.json`). Verification suite backs up/restores them.
- **Working tree is clean of tracked changes.** `git status --short` shows ONLY `__pycache__/*.pyc` files, which are gitignored (`__pycache__/` in `.gitignore`, confirmed via `git check-ignore`). Zero tracked-file diffs. No untracked files. No `.verify_snapshot/` (no `ACTIVE.json`, no `pending_snapshot.json`) — nothing to recover.
- Pinned data: `data/vintages.json` (2026-10-12 primary, 2026-10-11 committed), fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`. Cache coverage enforced by `scripts/check_data_coverage.py`.
- Prior handoffs at this repo state (identical content, no drift between 04-21/04-22/04-23 sessions): `HANDOFF_NEXT_SESSION_2026-10-29T04-23-42Z.md` is the previous pointer target.

## Clear Initial Task (Execute in Order)

Treat any failure as a blocker. Follow recovery procedures before making changes.

### 1) Confirm clean baseline
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 scripts/check_golden_baseline.py
SEED=42 python3 scripts/check_data_coverage.py
python3 -m unittest tests.test_portfolio_opt
```
All checks must pass. `scripts/check.sh` runs py_compile, JSON validation, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, experiment imports, and portfolio_opt tests.

### 2) Run quick verification (~8-10 min; use a long timeout or background)
```bash
SEED=42 python3 run_all_verification.py
```
If interrupted, recover:
```bash
SEED=42 python3 run_all_verification.py --restore-only
```
Or restore from git if needed: `git checkout -- experiments/` (use pinned commit if HEAD already contains a captured run).

### 3) Review open items & context
- Read `ledger/RESEARCH_LEDGER.md` (focus: E049, E041, E042-lead, E042 primary, E048, E045-E048)
- Review `ledger/golden_baseline.json` and `ledger/data_baseline.json` before any intentional re-pinning
- No new research warranted unless explicitly requested. Baseline guards are strict; never re-pin goldens to silence drift.
- E041 numeric drift (133 diffs) due to 1-ulp sensitivity; do not silence by re-pinning.
- Ledger inconsistency: E048 says E042-lead is unfixed and breaks the primary gate; E049 says it is fixed. Authoritative check is `run_all_verification.py` itself.

## Known Open Items
- **E041 numeric drift (133 diffs)** due to 1-ulp sensitivity of an ill-conditioned QP; do not silence by re-pinning.
- **E030/E029** offline-reproducible via pinned inputs.
- **Data coverage invariant**: new inputs must be committed and re-pinned.
- **Ledger inconsistency**: E048 vs E049 on E042-lead status. Read both; authoritative check is `run_all_verification.py`.
- **Research-engineering decision (ledger E049 open item)**: replace the SLSQP QP solves by a well-conditioned, deterministic solver (for N <= 5 an exact active-set enumeration of all KKT points is feasible and was used as the reference oracle), then re-pin the affected E041/E042 artifacts deliberately. Not started.
- **CI workflow cannot be created by agents.** Template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the actual workflow via the GitHub UI.

## Suggested First Command
```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```

## Current handoff pointer
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-29T05-06-00Z.md` (see also `HANDOFF_CURRENT.md`).