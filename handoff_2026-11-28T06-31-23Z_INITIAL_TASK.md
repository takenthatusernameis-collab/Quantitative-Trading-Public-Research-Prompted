# Agentic Handoff — Quantitative-Trading-Public-Research-Prompted

**Created:** 2026-11-28T06:31:23Z
**Session:** New session — 2026-11-28T06:31:23Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial task message for the next agentic work session

> Verify the research baseline is intact and reproduce the committed experiment drivers, then report any drift.
>
> Run the convention-robustness check first (fast, offline), then the quick verification suite:
>
> ```bash
> SEED=42 bash scripts/check.sh
> SEED=42 python3 run_all_verification.py --skip-slow
> ```
>
> If `scripts/check.sh` reports a golden mismatch under `experiments/`, fix it before committing — never let a verification run capture output into the canonical baseline. Recover with `SEED=42 python3 run_all_verification.py --restore-only` if a run was interrupted.
>
> Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect of running verification. Re-pinning is only warranted if a deliberate code change alters a published number, and that change must be recorded in `ledger/RESEARCH_LEDGER.md` first (see E050 precedent).
>
> Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. No new experiments should be started without re-opening the pre-registration/gating process.

## Key context

- `experiments/*.json` are committed golden artifacts; `run_all_verification.py` backs them up (`.verify_snapshot/`) before re-running and restores them afterwards — a run must never be left half-finished.
- `scripts/check_goldens_clean.py` fails when a tracked artifact under `experiments/` differs from HEAD or when a stale snapshot is pending.
- `scripts/check_golden_baseline.py` compares every artifact under `experiments/` with the SHA-256 fingerprint pinned in `ledger/golden_baseline.json`.
- `scripts/check_data_coverage.py` resolves every `data.download()` call site statically and requires each cache file be git-tracked and match the SHA-256 pinned in `ledger/data_baseline.json`. Unpinned inputs are live network downloads; yfinance is not bit-reproducible. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional; optimizer falls back to `scipy.optimize`.
- No separate linter configured; run `python3 -m py_compile` on changed files.
- Close-to-close is the v1.2.3 primary convention; overnight decomposition is reported alongside for every strategy.

## Never do

- Do not commit verification output / driver output into `experiments/`.
- Do not re-pin goldens as a side effect of verification.
- Do not gate on solver exit status in `src/portfolio_opt.py` — validate answers on problem constraints (see ledger E049/E050).
