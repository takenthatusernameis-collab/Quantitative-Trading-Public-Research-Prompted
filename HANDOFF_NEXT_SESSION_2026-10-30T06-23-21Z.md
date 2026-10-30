# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-10-30T06:23:21Z (UTC)
**Branch:** main
**Working tree:** clean for tracked source (only pre-existing `__pycache__/*.pyc` modifications; `experiments/` goldens match HEAD and pinned baseline).
**Snapshot:** `.verify_snapshot/` absent — no live verification run, nothing to recover.

## INITIAL TASK (do first)

**Verify baseline integrity before making any changes.**

```bash
SEED=42 bash scripts/check.sh
```

Expect exit 0. This runs: `py_compile` on core scripts/drivers, `check_goldens_clean.py` (working tree vs HEAD), `check_golden_baseline.py` (artifacts vs pinned SHA-256 in `ledger/golden_baseline.json`), `check_data_coverage.py` (all data inputs cached + pinned), and `tests/test_portfolio_opt.py`.

If it fails:
- Stale snapshot / goldens differ from HEAD with no live run owning it → recover: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` as last resort). Never leave a verification run half-finished.
- If a tracked artifact under `experiments/` was replaced in HEAD vs the pinned baseline, **do not re-pin by re-running verification**. Restore the correct artifact from the commit whose SHA-256 matches `ledger/golden_baseline.json` (`git checkout <commit> -- experiments/<file>`) and fix the cause. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff.

## Rules (follow strictly)

- Always use `SEED=42`. Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`); all required caches must be present and pinned.
- **Do not commit verification output.** Restore goldens before committing if interrupted.
- **Do not modify goldens (`experiments/*.json`) as a side effect of verification.** Never re-run experiments to "refresh" goldens. Do **not** re-pin to silence drift.
- **Do not commit changes without explicit user direction.**
- Sensitivity grids are reported, not gated; confirmatory runs require pre-registration + full placebo.
- CI workflow cannot be created by automated agents (template at `.github/workflow-templates/verification-gate.yml`).

## Known open items (only act on if explicitly asked)

- E041: 133 numeric diffs remain due to ill-conditioned tangency QP sensitivity (optimizer determinism rule fixed; 3 structural diffs eliminated). Do **not** re-pin to silence it. Open item per `ledger/RESEARCH_LEDGER.md` (E049).
- E041/E042 grid can drift by 1-ulp; do not re-pin artifacts to mask this.
- E029 and E030 are offline-reproducible with 0 differences.

## Quick reference commands

```bash
# Fast checks
SEED=42 bash scripts/check.sh
SEED=42 make check

# Verification
SEED=42 python3 run_all_verification.py --skip-slow  # convention + quick gates
SEED=42 python3 run_all_verification.py --quick       # 8 drivers + batch/validate + E042 n_sim=2
SEED=42 python3 run_all_verification.py --extended    # +18 drivers (reports drift in .verify_reports/)
SEED=42 python3 run_all_verification.py --full        # +E042 n_sim=50 + 96-config grid

# Recovery
SEED=42 python3 run_all_verification.py --restore-only

# Guards
SEED=42 python3 scripts/check_goldens_clean.py
SEED=42 python3 scripts/check_golden_baseline.py
SEED=42 python3 scripts/check_data_coverage.py
```

## Files to read first

- `AGENTS.md` (full project commands/conventions)
- `ledger/RESEARCH_LEDGER.md`
- `ledger/golden_baseline.json`
- `ledger/data_baseline.json`
- `scripts/check.sh`
- `run_all_verification.py`
