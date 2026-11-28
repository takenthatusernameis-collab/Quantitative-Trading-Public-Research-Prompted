# Agentic Work Session Handoff

**Timestamp**: 2026-11-28T06:33:24Z
**Session**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial task message for the next agentic work session

> Verify the research baseline is intact and reproduce the committed experiment
> drivers, then report any drift.
>
> Run the convention-robustness check first (fast, offline), then the
> quick/extended verification suite:
>
> ```bash
> SEED=42 bash scripts/check.sh
> SEED=42 python3 run_all_verification.py --extended
> ```
>
> If `scripts/check.sh` reports a golden mismatch under `experiments/`, fix it
> **before** committing — never let a verification run capture output into the
> canonical baseline. Recover with
> `SEED=42 python3 run_all_verification.py --restore-only` if a run was
> interrupted.
>
> Do **not** re-pin `ledger/golden_baseline.json` or
> `ledger/data_baseline.json` as a side effect of running verification.
> Re-pinning is only warranted if a deliberate code change alters a published
> number, and that change must be recorded in `ledger/RESEARCH_LEDGER.md`
> first (see the E050 precedent).
>
> Research phase is complete (E001–E043). Surviving validated strategies are
> documented in `ledger/RESEARCH_LEDGER.md`. Do not start new experiments
> without re-opening the pre-registration / gating process.

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US
equities, futures, and macro data. All experiments are pre-registered with
falsification expectations and promotion gates. **Research phase complete
(E001–E043).**

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh            # or: make check

# Quick full verification (~8 min; 8 drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py  # or: make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended   # or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full       # or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py      # or: make verify
```

## Key Context

- `experiments/*.json` are committed golden artifacts; `run_all_verification.py`
  backs them up (`.verify_snapshot/`, with an `ACTIVE.json` pid marker) before
  re-running and restores them afterwards — a run must never be left
  half-finished.
- `scripts/check_goldens_clean.py` fails when a tracked artifact under
  `experiments/` differs from HEAD or when a stale snapshot is pending.
- `scripts/check_golden_baseline.py` compares every artifact under
  `experiments/` with the SHA-256 fingerprint pinned in
  `ledger/golden_baseline.json`.
- `scripts/check_data_coverage.py` resolves every `data.download()` call site
  statically and requires each cache file be git-tracked and match the SHA-256
  pinned in `ledger/data_baseline.json`. Unpinned inputs are live network
  downloads; yfinance is not bit-reproducible. Verification runs with
  `QUANT_RESEARCH_OFFLINE=1`.
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy,
  pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional; the optimizer
  falls back to `scipy.optimize`.
- No separate linter configured; run `python3 -m py_compile` on changed files.
- Close-to-close is the v1.2.3 primary convention; overnight decomposition is
  reported alongside for every strategy.
- Optimizer determinism (ledger E049/E050): `src/portfolio_opt.py` validates a
  solver answer on the problem's constraints, never on the solver's exit
  status. Do not gate on solver exit status.

## Never Do

- Do not commit verification output / driver output into `experiments/`.
- Do not re-pin goldens as a side effect of verification.
- Do not gate on solver exit status in `src/portfolio_opt.py` — validate answers
  on problem constraints (see ledger E049/E050).

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment and baseline integrity.
2. Review `ledger/RESEARCH_LEDGER.md` for surviving validated strategies.
3. Run `SEED=42 python3 run_all_verification.py --extended` and report any drift.
4. If a golden mismatch appears, fix it before committing; never re-pin as a
   side effect of verification.