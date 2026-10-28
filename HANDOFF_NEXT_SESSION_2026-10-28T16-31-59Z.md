# Handoff — Timestamped clear initial task for next agentic session

Timestamp (UTC): 2026-10-28T16:31:59Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: 89fb201 (chore(kilo): checkpoint agent session)
Working dir: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Blocker to clear FIRST (stale verification snapshot)

`.verify_snapshot/ACTIVE.json` exists and owns pid **14924**, but that process is **no longer running** — a previous verification run was interrupted/killed. The suite refuses to start while a live snapshot is owned, and `experiments/` may hold driver output instead of committed goldens.

**Do not start a new verification run yet.** Recover first:
```bash
SEED=42 python3 run_all_verification.py --restore-only
```
Then confirm `git status --short` shows only tracked `__pycache__/*.pyc` as modified (no canonical artifacts changed).

## Current state (snapshot)

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` (goldens), pinned by `ledger/golden_baseline.json`. Do NOT modify them as a side effect of verification; never re-pin to silence numeric drift.
- Baseline integrity guards: `scripts/check_goldens_clean.py` (worktree vs HEAD), `scripts/check_golden_baseline.py` (vs pinned SHA-256s), `scripts/check_data_coverage.py` (35 pinned inputs vs `ledger/data_baseline.json`).
- Data coverage invariant enforced; pinned vintages in `data/vintages.json` (2026-10-12 primary, 2026-10-11 committed), E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`.
- Optimizer determinism rule pinned by `tests/test_portfolio_opt.py`; `src/portfolio_opt.py` validates on constraints, never solver exit status.
- Verification driver: `run_all_verification.py` (`--quick` / `--extended` / `--full` / `--skip-slow` / `--restore-only`). Always `SEED=42`.
- `__pycache__/*.pyc` files are tracked and show as modified on clean checkout — not a baseline concern; do not commit unless intentionally regenerated.
- Environment: dependencies installed at `/home/runner/work/_temp/kilo-home/.local`. Fresh session may need `pip install -r requirements.txt` again.

## Clear initial task for next session

Execute in order. Treat failures as blockers to fix before proceeding.

### 1) Recover stale snapshot (required first step)
```bash
SEED=42 python3 run_all_verification.py --restore-only
```
(Recovery uses repo-local `.verify_snapshot/` with `ACTIVE.json`; suite self-recovers at startup and refuses to start while another live run owns it.)

### 2) Verify clean baseline (must pass)
```bash
SEED=42 bash scripts/check.sh
```
Expected: py_compile, goldens clean vs HEAD, golden baseline pin match, data coverage, portfolio_opt tests all pass.

### 3) Run quick verification (recommended baseline)
```bash
SEED=42 python3 run_all_verification.py
```
If interrupted (SIGKILL/OOM/timeout), recover with `--restore-only` before anything else.

### 4) Review open items before making changes
- Read `ledger/RESEARCH_LEDGER.md` (focus E049 and active open items).
- Review `ledger/golden_baseline.json` / `ledger/data_baseline.json` before any intentional re-pinning.
- Open item: E041 numeric drift (~133 diffs) from ill-conditioned tangency QP (1-ulp sensitivity). Do NOT re-pin to silence it.

## Constraints / reminders (do not skip)
- Always use `SEED=42`.
- Never leave a verification run half-finished; if unsure, run `--restore-only`.
- If `scripts/check.sh` reports golden mismatch, fix before committing — never re-pin goldens as a side effect of running verification.
- CI workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml` (maintainer creates via GitHub UI). Local equivalents: `make check`, `make verify`, `make verify-quick`, `make verify-extended`, `make verify-full`.
- Follow `AGENTS.md` conventions (pre-registration, multiple-testing discipline, negative results recorded honestly).
- No new research is warranted unless explicitly requested.

## Suggested first commands (ready to run after recovery)
```bash
cat .verify_snapshot/ACTIVE.json 2>/dev/null; echo "---"
SEED=42 python3 run_all_verification.py --restore-only
git status --short
SEED=42 bash scripts/check.sh
```

## Current handoff pointer
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-28T16-31-59Z.md` (see also `HANDOFF_CURRENT.md` and `HANDOFF_NEXT_SESSION.md`).
