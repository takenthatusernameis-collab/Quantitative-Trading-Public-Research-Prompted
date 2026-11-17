# Handoff — agentic work session

**Created:** 2026-11-17T00:04:44Z
**Session:** kilo-auto/free
**Status:** Research phase complete (E001–E043). No active task in flight; working tree clean except regenerated `__pycache__` `.pyc` files (not tracked). Prior handoff `handoff_2026-11-17T00:03:20Z_INITIAL_TASK.md` superseded.

## Initial task for the next session

Continue verification-suite maintenance and drift triage for this quantitative-research repository. Concretely:

1. Run `SEED=42 bash scripts/check.sh` (fast) and confirm it passes — convention-robustness + template-validation gate.
2. Run `SEED=42 python3 run_all_verification.py --skip-slow` to re-execute the 8 quick drivers and confirm goldens restore cleanly. Never leave a verification run half-finished; the suite self-recovers at startup from `.verify_snapshot/` and refuses to start while a live run owns it.
3. Inspect `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (if present from a prior `--extended` run) and triage drift: E041 is expected to still report ~133 numeric differences (1-ulp QP sensitivity, ledger E049) — **do not re-pin** it. E029/E030 should reproduce with 0 differences (inputs pinned).
4. If any *new* structural drift appears, root-cause it before touching `experiments/*.json`. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` and a ledger entry.

## Context

- Repo: `Quantitative-Trading-Public-Research-Prompted`. Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, macro data.
- `experiments/*.json` are committed golden artifacts. `run_all_verification.py` backs them up before re-running and restores them afterward — **never commit verification output**. Recovery: `SEED=42 python3 run_all_verification.py --restore-only`.
- Cache coverage is an enforced invariant: `scripts/check_data_coverage.py` resolves every `data.download()` call site and requires each cache file to exist, be git-tracked, and match the SHA-256 in `ledger/data_baseline.json`. Verification re-executes every driver with `QUANT_RESEARCH_OFFLINE=1`.
- Optimizer determinism rule is pinned by `tests/test_portfolio_opt.py` (part of `scripts/check.sh`): tangency QP validated on the problem's constraints, never on the solver's exit status.
- Convention: close-to-close is v1.2.3 primary; overnight decomposition reported alongside. Seed always `SEED=42`.
- Lint: no separate linter; run `python3 -m py_compile` on changed files.

## Quick commands

- `SEED=42 bash scripts/check.sh` — fast convention-robustness check + template validation
- `SEED=42 python3 run_all_verification.py --skip-slow` — convention-only, skip slow batch/regression
- `SEED=42 python3 run_all_verification.py --extended` / `--full` — extended/full verification
- `SEED=42 python3 run_all_verification.py --restore-only` — recover goldens after an interrupted run
- `python3 scripts/check_data_coverage.py` / `python3 scripts/check_golden_baseline.py --update` — re-pin data/golden baselines

## Known open items

- E041 still reports 133 numeric differences (1-ulp QP sensitivity); do not re-pin to silence — see ledger E049/open item.
- E030/E029 reproduce with 0 differences since 2026-10-20 (pinned inputs).
- CI gate (`.github/workflows/verification-gate.yml`) cannot be created by automated agents; copyable template at `.github/workflow-templates/verification-gate.yml`, needs a maintainer to create the real workflow via the GitHub UI.

## State of the working tree

- `git status` shows only regenerated `__pycache__/*.pyc` (not tracked). No source or artifact changes.
- `research_state/workflow_run_diagnostics.jsonl` and `workflow_backups/*.bak` are runtime/local artifacts, not part of the canonical baseline.

No pending blockers. If a verification run is interrupted, restore before committing (`run_all_verification.py --restore-only` or `git checkout -- experiments/`).
