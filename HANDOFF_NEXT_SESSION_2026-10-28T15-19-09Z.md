# HANDOFF — Timestamped clear initial task for next agentic session

Timestamp (UTC): 2026-10-28T15-19-09Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: 0e1a005
Working tree: clean (git status --short empty)
Verify snapshot: none active (.verify_snapshot/ACTIVE.json absent)

## Mission for next session
Start here and verify baseline integrity before making any changes. This repo is in post-research state (E001–E043) with strict baseline/verification guards. No new research is warranted unless explicitly requested.

## Current known state
- Research complete; surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- Verification guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- Optimizer determinism pinned by `tests/test_portfolio_opt.py`
- Data: pinned vintages `data/vintages.json` (2026-10-12), committed 2026-10-11 vintage, E029 fundamentals pinned in `data/fundamentals/`
- Verification driver: `run_all_verification.py` (`--quick`/`--extended`/`--full`/`--skip-slow`/`--restore-only`)
- CI workflow cannot be created by agents. Template at `.github/workflow-templates/verification-gate.yml`.

## Immediate priorities (do in order)
1. **Clean baseline** — Run `git status --short`. If any tracked files differ, do **not** re-pin goldens.
2. **Sanity check** — Run `SEED=42 bash scripts/check.sh`. All must pass.
3. **Verify reproducibility** — Quick: `SEED=42 python3 run_all_verification.py`; Extended: `--extended` (E041 drift, do not re-pin).
4. **Recovery if interrupted** — `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.

## Known open items
- **E041 numeric drift (133 diffs)** due to 1-ulp sensitivity; do not silence by re-pinning.
- **E030/E029** offline-reproducible via pinned inputs.
- **Data coverage invariant**: new inputs must be committed and re-pinned.

## Suggested first command
```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```

## Current handoff pointer
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-28T15-19-09Z.md` (see also `HANDOFF_CURRENT.md`).

(End of file)
