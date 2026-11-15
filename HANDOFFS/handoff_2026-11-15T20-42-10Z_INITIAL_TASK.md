# Durable Handoff — Initial Task for Next Agentic Session

- **Timestamp (UTC):** 2026-11-15T20:42:10Z
- **HEAD:** `a9eda5cc563d2d6ae478126a6533c2d7d84a7089` (`chore(kilo): checkpoint agent session`, main)
- **Remote sync:** `git rev-list --left-right --count origin/main...HEAD` → `0 0` (in sync, `origin/main` == `a9eda5cc`)
- **Prior handoff superseded:** `handoff_2026-11-15T19-53-51Z_INITIAL_TASK.md` (retained for history)

## Repository state
- Research phase **complete/closed**: E001–E051. Ledger durable-handoff refreshes recorded through **E393** (HEAD `15e283e7`) before this session; this handoff is logged as **E394**. See `ledger/RESEARCH_LEDGER.md`. No research task is open.
- No interrupted verification run: `.verify_snapshot/` and `.verify_reports/` are **absent**.
- Working tree before this deliverable: only pre-existing modified `__pycache__/*.pyc` files under `scripts/`, `src/`, `tests/` (gitignored build artifacts; **do not commit** — 15 `.pyc` paths are tracked in HEAD and show as ` M`, which is expected churn). No untracked files. No research-source, experiment, data, golden, or ledger content changed.

## Baseline integrity (re-verified this session, per-step isolation, no verification suite run)
All **exit 0**:
- `python3 scripts/check_json_artifacts.py` — 114 committed JSON artifacts parse OK
- `python3 scripts/check_goldens_clean.py` — committed golden artifacts match HEAD
- `python3 scripts/check_golden_baseline.py` — all 107 pinned golden artifacts match baseline fingerprint
- `python3 scripts/check_data_coverage.py` — all 35 pinned data inputs present, tracked, unchanged
- `python3 scripts/validate_template.py` — OK
- `python3 scripts/check_experiment_imports.py` — all experiment script imports/calls OK
- `SEED=42 python3 verify_convention_robustness.py` — all strategy blocks PASS (`ALL VERIFICATIONS PASSED`)

**Not run (sandbox dependency gap):** unit tests / full verification requiring `numpy`, `pandas`, `scipy`, `pytest` — not installed here (`ModuleNotFoundError: No module named 'numpy'/'pytest'`). Environment constraint, not a repo regression. Run `pip install -r requirements.txt` first.

## Known open items / caveats (do not "fix" without pre-registration)
- **E041/E042 grid artifacts**: residual 1-ulp optimizer sensitivity (ill-conditioned QP) causes numeric drift beyond tolerance in `--extended`; structural/gate decisions unchanged (E041 REJECTED 3/5). **Do not re-pin** these goldens to silence drift (ledger E049 + open item).
- **Optimizer determinism rule** (ledger E049): `src/portfolio_opt.py` validates a solver answer on the problem's *constraints*, never on the solver exit status; pinned by `tests/test_portfolio_opt.py` (a `scripts/check.sh` step).
- **Extended drift report**: `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` is gitignored / reporting-only when produced by `--extended`.
- **CI workflow**: intended gate `.github/workflows/verification-gate.yml` cannot be created by automated agents here (controller cleans `.github/workflows/`; token lacks `workflows` scope). A maintainer must add it via GitHub UI from `.github/workflow-templates/verification-gate.yml`; see `VERIFICATION_GATE_TEMPLATE.md`.
- **Golden restore**: if a verification run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`, or `git checkout -- experiments/`. Note `git checkout` restores whatever `HEAD` holds — if a checkpoint commit ever captures verification output, restore the pinned artifact instead (`git checkout <commit> -- experiments/<file>`, where `<commit>` is the last whose SHA-256 matches `ledger/golden_baseline.json`).

## Reproduction / verification commands
```bash
pip install -r requirements.txt                  # if deps missing (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
SEED=42 bash scripts/check.sh                    # fast guards + template validation (~seconds, offline)
SEED=42 python3 run_all_verification.py                     # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended          # ~21 min
SEED=42 python3 run_all_verification.py --full              # ~15 min
SEED=42 python3 verify_convention_robustness.py
```

## Guardrails
- Always `SEED=42`.
- Never commit verification output; never modify `experiments/*.json` goldens except an explicit, reviewed re-pin via `python3 scripts/check_golden_baseline.py --update` (never to silence drift).
- Do not move pre-registered goalposts, gates, sensitivity grids, or validated constructions post-hoc. Negative results stay recorded honestly (REJECTED / PARTIAL).
- `__pycache__/`, `.verify_snapshot/`, `.verify_reports/` are not research artifacts to commit.
- Re-pin data inputs only via `python3 scripts/check_data_coverage.py --update` after committing the new file.

## Clear initial task for next session
**No research action required.** The repository is clean, closed (E001–E051), and guard-verified as of `a9eda5cc`.
1. Confirm environment parity first: `pip install -r requirements.txt` (if needed), then `SEED=42 bash scripts/check.sh`.
2. Only start new work on an explicit, pre-registered research request or a maintenance directive from the user; otherwise report status and await instructions.
3. If asked about reproducibility/drift, prefer read-only checks first. Do not re-run drivers, re-pin baselines, or commit anything unless explicitly directed and justified per ledger policy.
4. This file is the canonical handoff; mirror pointers (`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`, and the root aliases) are repointed by `python3 scripts/repoint_handoff.py handoff_2026-11-15T20-42-10Z_INITIAL_TASK.md`.