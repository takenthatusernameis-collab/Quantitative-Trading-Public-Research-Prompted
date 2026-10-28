# HANDOFF — Timestamped initial task for next agentic session

Timestamp (UTC): 2026-10-28T14-33:00Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: 331e03f (chore(kilo): checkpoint agent session)
Working tree: clean except __pycache__ (gitignored); check with `git status --short`
Verify snapshot: none active (.verify_snapshot/ACTIVE.json absent)

## Mission for next session
Start here and verify baseline integrity before making any changes. This repo is in post-research state (E001–E043) with strict baseline/verification guards. No new research is warranted unless explicitly requested.

## Current known state
- Research complete; surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- Baseline verified: `SEED=42 bash scripts/check.sh` ALL CHECKS PASSED (confirmed 2026-10-28T14:33Z)
- Golden baseline pin matches HEAD: `python3 scripts/check_golden_baseline.py` → 107/107 artifacts match (exit 0)
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

## Session event log (this session)
- Confirmed clean baseline: `check.sh` ALL CHECKS PASSED; `check_golden_baseline.py` 107/107 match.
- Attempted quick verification; it exceeded the 600 s tool timeout and was interrupted. Snapshot existed (pid 50576) with 5 tracked artifacts modified.
- Recovered with `--restore-only`; working tree clean, snapshot gone.
- Note: the quick suite takes >10 min. Use a longer timeout or run in background next time.

## Known open items
- **E041 numeric drift (133 diffs)** due to 1-ulp sensitivity; do not silence by re-pinning.
- **E030/E029** offline-reproducible via pinned inputs.
- **Data coverage invariant**: new inputs must be committed and re-pinned.
- **Ledger inconsistency**: E048 says E042-lead is unfixed and breaks the primary gate; E049 says it is fixed. Read both before deciding; the authoritative check is `run_all_verification.py` itself.

## Suggested first command
```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```

## Current handoff pointer
This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-28T14-33-00Z.md` (see also `HANDOFF_CURRENT.md`).