# HANDOFF — Timestamped clear initial task for next agentic session

Timestamp (UTC): 2026-10-28T16:13:42Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: f80f8d5 (chore(kilo): checkpoint agent session)
Working tree: clean except tracked __pycache__/*.pyc files (no canonical artifacts changed)
Verify snapshot: none active (.verify_snapshot/ absent)

## Mission for next session
This repo is in post-research state (E001–E043 complete). Surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. Baseline/verification guards are strict: never leave a verification run half-finished, never re-pin goldens as a side effect of verification. No new research is warranted unless explicitly requested. Start by confirming baseline integrity before making any changes.

## Current known state
- Research complete; canonical artifacts are `experiments/*.json`, pinned by `ledger/golden_baseline.json`.
- Data coverage invariant enforced by `scripts/check_data_coverage.py` against `ledger/data_baseline.json`; pinned vintages in `data/vintages.json` (2026-10-12 primary, 2026-10-11 committed), E029 fundamentals pinned in `data/fundamentals/`.
- Optimizer determinism rule pinned by `tests/test_portfolio_opt.py`; `src/portfolio_opt.py` validates on constraints, never solver exit status.
- Verification driver: `run_all_verification.py` (`--quick` / `--extended` / `--full` / `--skip-slow` / `--restore-only`). Always `SEED=42`.
- CI workflow cannot be created by agents. Local equivalents: `make check`, `make verify`, `make verify-quick`, `make verify-extended`, `make verify-full`. Template at `.github/workflow-templates/verification-gate.yml`.

## Immediate priorities (do in order)
1. **Clean baseline** — `git status --short`. Only __pycache__ .pyc files should show; if any tracked artifact under `experiments/` or `ledger/` differs, do NOT re-pin. Restore if a prior run was interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
2. **Sanity check** — `SEED=42 bash scripts/check.sh` (all must pass; includes `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `test_portfolio_opt.py`).
3. **Verify reproducibility** — Quick: `SEED=42 python3 run_all_verification.py`. Extended: `--extended` (reports E041 drift, do not re-pin).
4. **Recovery if interrupted** — `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. The suite self-recovers at startup and refuses to start while another live run owns `.verify_snapshot/`.

## Known open items
- **E041 numeric drift (~133 diffs)**: 1-ulp sensitivity of the ill-conditioned tangency QP in `src/portfolio_opt.py`. Do NOT re-pin to silence. Root cause already fixed (E049); remaining drift is inherent to the problem.
- **E030 / E029**: offline-reproducible since 2026-10-20 via committed/pinned inputs (ETF panel + fundamentals snapshot).
- **Ledger E048 vs E049**: E048 says E042-lead is unfixed and breaks the primary gate; E049 says it is fixed. Read both before deciding. Authoritative check is `run_all_verification.py` itself.
- **__pycache__ .pyc files are tracked** and show as modified on a clean checkout. Not a baseline concern; do not commit them unless intentionally regenerated.

## Suggested first command
```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```

## Current handoff pointer
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-28T16-13-42Z.md` (see also `HANDOFF_CURRENT.md` and `HANDOFF_NEXT_SESSION.md`).