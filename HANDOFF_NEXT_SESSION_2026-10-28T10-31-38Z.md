# HANDOFF_NEXT_SESSION_2026-10-28T10-31-38Z

**Created:** 2026-10-28T10:31:38Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working tree:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Source:** HANDOFF.md (updated 2026-10-28T10:25:29Z)

## Initial Task (do this first)

You are taking over a clean, verified baseline. Do **not** re-run experiments to "update" goldens unless explicitly asked. Follow the guards below.

### 1) Verify baseline integrity (required)

Run the convention-robust fast check first:

```bash
SEED=42 bash scripts/check.sh
```

Expected: all checks pass (py_compile, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `tests/test_portfolio_opt.py`).

If any guard fails, **stop and recover**. See AGENTS.md "Baseline Integrity". Never re-pin as a side effect of verification.

### 2) (Recommended) Sanity check verification path

If you need confidence the suite is healthy:

```bash
SEED=42 python3 run_all_verification.py   # quick (~8 min)
```

Or `make verify-quick`. Do **not** commit any verification output. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

### 3) Know the active caveats

- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates on problem constraints (not solver status). SLSQP status 8 is acceptable. Tangency QP is ill-conditioned → E041/E042 grid may show numeric drift (~1e-5). Structural differences must remain zero. Do **not** re-pin to silence numeric drift.
- **Extended drift reporting:** `--extended` writes `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored). E029 fundamentals and E030 ETF panel are pinned/offline-reproducible; E041 drift remains open (133 numeric diffs > 1e-4 tolerance, structural fixed).
- **Data coverage enforced:** every `data.download()` must have a committed, git-tracked cache file pinned in `ledger/data_baseline.json`. Missing/unpinned inputs fail hard under offline verification.
- **Golden discipline:** `experiments/*.json` are canonical. Verification backs up/restores them. Re-pinning requires `scripts/check_golden_baseline.py --update` with intent.

## Read first

- `AGENTS.md` — full commands, guards, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — research state, decisions (REJECTED/PARTIAL), open items
- `ledger/golden_baseline.json` and `ledger/data_baseline.json` — pinned fingerprints
- `scripts/check.sh` — the gate you must satisfy

## Immediate focus

Determine if there is any open work from the ledger (e.g. E041 numeric drift follow-up) or if you are asked to run verification/reproduce. If no explicit task is given beyond this handoff, **run (1) above and report status only**. Do not make speculative changes.

**End of handoff.**
