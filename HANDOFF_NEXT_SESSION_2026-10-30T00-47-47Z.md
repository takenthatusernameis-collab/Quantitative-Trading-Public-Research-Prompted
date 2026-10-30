# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-30T00:47:47Z (message time)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `bd82575` (2026-10-30 00:47:39 +0000, "chore(kilo): checkpoint agent session")
**Preceding handoff:** `HANDOFF_NEXT_SESSION_2026-10-30T00-42-23Z.md`

## Current State (verified at handoff time)

- **Working tree:** clean of tracked changes. Only `__pycache__/*.pyc` modified (gitignored build artifacts from compile checks). `git status --short` shows no tracked source/data modifications.
- **No live snapshot:** `.verify_snapshot/` absent, no `ACTIVE.json`. No verification run in progress; nothing to recover.
- **Experiment artifacts:** 107 committed JSONs under `experiments/` (E001–E043, plus blends/auxiliary). All match HEAD.
- **Research phase:** complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Guards in place and expected green:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `tests/test_portfolio_opt.py`, `verify_convention_robustness.py`, template validation, experiment-script imports.

## Initial Task (Start Here)

There is **no new research task**. The repository is fully verified and stable. Before doing any new work, establish and confirm a clean baseline:

1. **Verify guards pass**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Must complete with all checks green (goldens clean vs HEAD, golden baseline SHA-256 match, data coverage, portfolio-opt tests, py_compile, etc.).

2. **Confirm tree state**
   ```bash
   git status --short && git diff --name-only
   ```
   Only untracked/build-artifact `__pycache__/*.pyc` allowed; no tracked source modifications.

3. **Recover if interrupted**
   If `experiments/*.json` are dirty from a previous interrupted run, restore:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   (or `git checkout -- experiments/`). The suite self-recovers at startup and refuses to start while another live run owns the snapshot.

## Known Pre-Existing Drift (reporting-only, decisions unchanged)

Do **not** re-pin goldens or baselines to silence these — committed baselines are authoritative.

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). The 3 structural differences are gone. Open item in the ledger.
- **E030**: numeric diffs on near-zero quantities (documented, ledger E048). Its 16-ETF input is committed and the golden was deliberately re-pinned.
- **E029**: offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`); golden deliberately re-pinned. Reproduces with 0 differences.

## Constraints (Do Not Violate)

- Always use `SEED=42`.
- Never leave `run_all_verification.py` half-finished. `.verify_snapshot/` with `ACTIVE.json` is used for recovery; a killed run stays recoverable.
- Do **not** re-pin goldens or `ledger/golden_baseline.json` / `ledger/data_baseline.json` to silence drift — the committed golden is the authoritative record, not the latest re-run.
- Do **not** commit verification outputs (`.verify_reports/`, driver re-runs). Only commit intentional source/data changes.
- Honor pinned cache vintages (`data/vintages.json`, `data/fundamentals_vintages.json`). Verification runs with `QUANT_RESEARCH_OFFLINE=1`; a missing cache entry fails hard instead of silently downloading.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

## Suggested Next Actions

- Read `AGENTS.md` (quick start, baseline integrity, reproducibility) and `ledger/RESEARCH_LEDGER.md` to understand current state.
- If the user supplies a new task, execute it within the constraints above. If no task is supplied, the correct action is to confirm the baseline is clean and stop — do not invent work.
- If a verification run is requested, prefer `SEED=42 python3 run_all_verification.py --extended` (~21 min) and expect the E030/E041 drift above.

## Quick Commands

```bash
SEED=42 bash scripts/check.sh                                              # fast offline guard suite
SEED=42 python3 run_all_verification.py                      # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended           # (~21 min)
SEED=42 python3 run_all_verification.py --full              # (~15 min)
SEED=42 python3 run_all_verification.py --skip-slow         # convention only
SEED=42 python3 run_all_verification.py --restore-only      # recover if interrupted
SEED=42 python3 verify_convention_robustness.py             # convention robustness only
```
