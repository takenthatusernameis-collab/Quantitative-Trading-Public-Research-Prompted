# Handoff (timestamp: 2026-11-01T05:29:13Z)

## INITIAL TASK (Start here)
**Goal:** Repository baseline is verified and stable. No new research task is active.
Confirm the baseline remains clean and report. Do not modify goldens, weaken
tolerances, or change gate logic.

Execute in order:

1. [ ] **Check repo state** - `git status && git log -1 --oneline`
2. [ ] **Run fast integrity check** - `SEED=42 bash scripts/check.sh`
     - Confirm `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` pass
     - Confirm `scripts/check_data_coverage.py` passes
     - Confirm tests pass (`tests/test_portfolio_opt.py`; `python3 -m py_compile` on changed files)
3. [ ] **Recover if needed** - If goldens differ or a snapshot is stale, run
     `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
     Never proceed with modified goldens.
4. [ ] **Review open items** - Read `ledger/RESEARCH_LEDGER.md` (E049 optimizer determinism;
     E041/E042 QP drift must not be re-pinned to silence).
5. [ ] **Report baseline status** - Summarize pass/fail and confirm baseline clean.

## Baseline Status (verified 2026-11-01T05:29:13Z)
- `SEED=42 bash scripts/check.sh` -> **ALL VERIFICATIONS PASSED** (exit OK), incl. the
  E042 min-var confirmatory gate (PARTIAL 4/5 as recorded — G2 placebo-significance
  fails; not promoted).
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`,
  `scripts/check_data_coverage.py` all pass. `tests/test_portfolio_opt.py` passes;
  all experiment driver imports OK.
- Working tree: clean of tracked source changes (only gitignored `__pycache__/*.pyc`
  bytecode diffs). No live verification snapshot (`.verify_snapshot/` absent).
  Nothing to recover.
- HEAD: `0e62fc6 chore(kilo): checkpoint agent session` on `main`, up to date with
  `origin/main`.

## Project State (from AGENTS.md)
- Repo: Quantitative-Trading-Public-Research-Prompted. Research phase complete
  (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Golden artifacts: `experiments/*.json` canonical. Verification backs up/restores via
  `.verify_snapshot/`; never leave a verification run half-finished.
- Data coverage pinned in `ledger/data_baseline.json`; E029 fundamentals pinned;
  E030 panel committed. Offline reproducibility enforced (`QUANT_RESEARCH_OFFLINE=1`).
- Pre-registration, multiple-testing discipline, negative results recorded honestly.

## Known pre-existing drift (reporting-only, decisions unchanged)
- **E041**: ~133 numeric diffs (1-ulp sensitivity of ill-conditioned QP; optimizer
  determinism fixed per ledger E049). 3 structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E042**: residual ill-conditioning of the tangency QP (ledger E049 open item);
  `min_var` answers still move by up to ~2.6e-05 at the 1-ulp level. Do **not** re-pin.

## Constraints
- Always use `SEED=42`.
- Do not commit verification output; restore goldens if interrupted.
- Do not re-pin goldens as a side effect of verification.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated
  constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, src/macro.py`,
  `src/portfolio_opt.py`).
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- CI workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml`.

## Quick Commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --skip-slow
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py --restore-only
```

## Notes
- No prior task work performed this session beyond baseline verification; the
  integrity check passed and the working tree is clean of tracked changes.
- Durable symlinks (root and `.kilo/`): `handoff.md`, `handoff_current.md`,
  `handoff_next.md`, `handoff_next_session.md`, `HANDOFF.md`, `HANDOFF_CURRENT.md`,
  `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md`, `HANDOFF_NEXT_SESSION_LATEST.md`
  point here.

(End of handoff)