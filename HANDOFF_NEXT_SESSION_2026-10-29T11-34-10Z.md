# Handoff for Next Agentic Session
- Timestamp (UTC): 2026-10-29T11:34:10Z
- Repo: Quantitative-Trading-Public-Research-Prompted
- Branch: main
- HEAD: 79a0783 (chore(kilo): checkpoint agent session)

## Initial Task (Clear & Actionable)
**START HERE:** Confirm baseline integrity before making any changes.

```bash
SEED=42 bash scripts/check.sh
```

- If this passes: report a clean status summary (goldens clean, golden baseline SHA match, data coverage OK, convention robustness OK, tests pass).
- If this fails: stop, report the exact failing step and remediation per `AGENTS.md`. Do not proceed until resolved.

## Current State
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Verification infrastructure in place: `run_all_verification.py`, `scripts/check.sh`, `make verify-quick/extended/full`.
- Baseline integrity guards active: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`. Snapshots live in `.verify_snapshot/` (gitignored) with `ACTIVE.json`.
- Golden artifacts under `experiments/` are authoritative; verification re-runs drivers and restores them. Never commit driver re-runs of goldens without re-pinning via ledger-approved process.

## Open Items / Known Gotchas
- **E041 drift / optimizer determinism (ledger E049):** SLSQP status gating fixed to validate constraints (not solver exit status), pinned by `tests/test_portfolio_opt.py`. Tangency QP remains ill-conditioned → E041 grid still shows numeric drift (133 diffs); extended block still reports drift. **Do not re-pin E041 goldens to silence this.** Track in ledger.
- **E030 / data reproducibility:** Pinned vintages in `data/` and E029 fundamentals in `data/fundamentals/` per `data/fundamentals_vintages.json`. Data coverage enforced by `scripts/check_data_coverage.py`. E030 reproduces with 0 differences.
- **Baseline pinning discipline:** If any tracked artifact under `experiments/` must change, re-pin via `python3 scripts/check_golden_baseline.py --update` (and ensure it appears in the diff). Never do this as a side effect of the verification suite.
- **Snapshot hygiene:** If a previous run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`. Ensure `.verify_snapshot/ACTIVE.json` is absent before starting a fresh run.

## Recommended Next Actions
1. **Integrity check (required)** - `SEED=42 bash scripts/check.sh`
2. **Quick sanity verification** - If clean: `SEED=42 python3 run_all_verification.py --quick` (or `make verify-quick`). Prefer `--quick` before `--extended`/`--full`.
3. **Review context** - Read `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, and `ledger/data_baseline.json` if planning to change artifacts.
4. **Wait for direction** - If no specific user task is provided, stop at step 1 summary. If a new research task is given, follow pre-registration, multiple-testing discipline, and all baseline protection rules.

## Notes
- **CI:** Workflow cannot be created by agents (controller restores `.github/workflows/`; token lacks `workflows` permission). Template at `.github/workflow-templates/verification-gate.yml`.
- **Conventions:** Close-to-close v1.2.3 primary; overnight decomposition reported.
- **Deps:** `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional (falls back to scipy).
- **Always:** Use `SEED=42`. Never leave verification half-finished. Never commit verification driver re-runs of goldens without ledger-approved re-pinning.
