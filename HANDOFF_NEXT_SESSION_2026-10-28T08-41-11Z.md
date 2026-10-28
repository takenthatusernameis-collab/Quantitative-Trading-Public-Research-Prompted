# HANDOFF — Timestamped initial task for next agentic session

Timestamp (UTC): 2026-10-28T08-41-11Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: 4f24588b0de72aabfe64ee753b5b21e78ca2b571
Working tree: 16 modified/untracked files
Verify snapshot: none

## Mission for next session
Start here and verify baseline integrity before making any changes. This repo is in post-research state (E001–E043) with strict baseline/verification guards. No new research is warranted unless explicitly requested.

## Current known state
- Research complete; surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- Baseline verified: `SEED=42 bash scripts/check.sh` passes; `SEED=42 python3 run_all_verification.py` (quick) passes
- Verification guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- Optimizer determinism pinned by `tests/test_portfolio_opt.py` (solver exit status must not gate feasibility/optimality)
- Data: pinned vintages `data/vintages.json` (2026-10-12), committed 2026-10-11 vintage, E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- Verification driver: `run_all_verification.py` (`--quick`/`--extended`/`--full`/`--skip-slow`/`--restore-only`). Backups in `.verify_snapshot/` (gitignored) with `ACTIVE.json` marker.
- CI workflow cannot be created by agents (controller restores `.github/workflows/`, token lacks `workflows` push). Template at `.github/workflow-templates/verification-gate.yml`.

## Immediate priorities (do in order)
1. **Clean baseline** — Run `git status --short`. If any tracked files differ, do **not** re-pin goldens. Follow AGENTS.md baseline integrity rules.
2. **Sanity check** — Run `SEED=42 bash scripts/check.sh` (convention-robustness + template validation + golden/data/coverage guards). All must pass.
3. **Verify reproducibility (choose scope)** — If check passes:
   - Quick (~8 min): `SEED=42 python3 run_all_verification.py`
   - Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended` (E041 still has numeric drift; do **not** re-pin)
   - Full (~15–30 min): only if explicitly needed
4. **Recovery if interrupted** — If verification was cut off or goldens look modified: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. Confirm `.verify_snapshot/ACTIVE.json` removed.

## Known open items
- **E041 numeric drift (133 diffs)** due to 1-ulp sensitivity of ill-conditioned tangency QP. Structural diffs resolved, gates/decision unchanged. Open in ledger; do **not** silence by re-pinning.
- **E030/E029** now offline-reproducible via pinned inputs; do not revert to live yfinance downloads.
- **Data coverage invariant**: any new `data.download()` inputs must be committed and re-pinned via `python3 scripts/check_data_coverage.py --update`.

## Suggested first command
```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```

## Current handoff pointer
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-28T08-41-11Z.md`
(End of file)
