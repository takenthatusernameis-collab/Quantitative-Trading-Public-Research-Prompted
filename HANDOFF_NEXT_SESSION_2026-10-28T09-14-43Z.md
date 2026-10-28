# HANDOFF — Timestamped initial task for next agentic session

Timestamp (UTC): 2026-10-28T09-14-43Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: see `git rev-parse HEAD`
Working tree: verify with `git status --short`
Verify snapshot: none

## Mission for next session
Start here and verify baseline integrity before making any changes. This repo is in post-research state (E001–E043) with strict baseline/verification guards. No new research is warranted unless explicitly requested.

## Current known state
- Research complete; surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- Baseline verified: `SEED=42 bash scripts/check.sh` passes; `SEED=42 python3 run_all_verification.py` (quick) passes
- Verification guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- Optimizer determinism pinned by `tests/test_portfolio_opt.py`
- Data: pinned vintages `data/vintages.json` (2026-10-12), committed 2026-10-11 vintage, E029 fundamentals pinned in `data/fundamentals/`
- Verification driver: `run_all_verification.py` (`--quick`/`--extended`/`--full`/`--skip-slow`/`--restore-only`). Backups in `.verify_snapshot/` (gitignored) with `ACTIVE.json` marker.
- CI workflow cannot be created by agents. Template at `.github/workflow-templates/verification-gate.yml`.

## Immediate priorities (do in order)
1. **Clean baseline** — Run `git status --short`. If any tracked files differ, do **not** re-pin goldens. Follow AGENTS.md baseline integrity rules.
2. **Sanity check** — Run `SEED=42 bash scripts/check.sh`. All must pass.
3. **Verify reproducibility (choose scope)** — If check passes:
   - Quick (~8 min): `SEED=42 python3 run_all_verification.py`
   - Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended` (E041 still has numeric drift; do **not** re-pin)
   - Full: only if explicitly needed
4. **Recovery if interrupted** — `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. Confirm `.verify_snapshot/ACTIVE.json` removed.

## Known open items
- **E041 numeric drift (133 diffs)** due to 1-ulp sensitivity of ill-conditioned tangency QP. Structural diffs resolved, gates/decision unchanged. Do **not** silence by re-pinning.
- **E030/E029** now offline-reproducible via pinned inputs; do not revert to live yfinance downloads.
- **Data coverage invariant**: any new `data.download()` inputs must be committed and re-pinned via `python3 scripts/check_data_coverage.py --update`.

## Suggested first command
```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```

## Current handoff pointer
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-28T09-14-43Z.md`
(End of file)
