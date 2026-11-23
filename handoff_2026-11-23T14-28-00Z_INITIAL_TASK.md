# Handoff — Agentic Work Session

**Timestamp:** 2026-11-23T15:27:06Z
**Workspace:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Git repo:** yes (clean working tree expected)

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Files

- `ledger/RESEARCH_LEDGER.md` — canonical record of all experiments (E001–E043) with dispositions
- `ledger/golden_baseline.json` — SHA-256 fingerprints of committed golden artifacts under `experiments/`
- `ledger/data_baseline.json` — SHA-256 fingerprints of committed data cache files under `data/`
- `experiments/*.json` — committed golden artifacts (canonical research outputs)
- `scripts/check.sh` — fast offline integrity check (py_compile, convention robustness, golden cleanliness, golden baseline match, data coverage)
- `run_all_verification.py` — full verification suite with backup/restore of golden artifacts
- `src/batch_run.py`, `src/validate.py` — core batch drivers
- `experiments/run_e*.py` — individual experiment drivers

## Critical Invariants

1. **Never leave a verification run half-finished** — it overwrites `experiments/*.json` and restores them on completion. If killed, recover with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
2. **Golden baseline is authoritative** — `ledger/golden_baseline.json` pins SHA-256 of every artifact. Re-pinning requires deliberate ledger entry first (`python3 scripts/check_golden_baseline.py --update`).
3. **Data cache coverage enforced** — `scripts/check_data_coverage.py` validates every `data.download()` call site resolves to a committed, SHA-256-pinned cache file. Unpinned inputs fail hard under `QUANT_RESEARCH_OFFLINE=1`.
4. **Seed always 42** — walk-forward + placebo RNG.
5. **Convention** — close-to-close primary (v1.2.3), overnight decomposition reported alongside.

## Recent Ledger Entries (E045–E050)

- **E045**: E029 offline-reproducible (fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`)
- **E048**: E030 panel committed (16-ETF input), golden re-pinned
- **E049**: Optimizer determinism root-caused — SLSQP status 8 gating removed; validate on constraints not exit status
- **E050**: Exact KKT active-set enumeration as primary tangency solver → bit-reproducible artifacts (E041/E042 now 0 differences)

## Next Session Suggestions

- Run `SEED=42 bash scripts/check.sh` to verify workspace integrity
- Run `SEED=42 python3 run_all_verification.py --skip-slow` for fast convention-only check
- If extending research: pre-register new experiment per conventions, add driver under `experiments/`, update ledger
- If modifying optimizer/portfolio code: run `python3 -m pytest tests/test_portfolio_opt.py` (part of `scripts/check.sh`)

## Environment

- Python 3, deps: `numpy`, `pandas`, `scipy`, `pyarrow`, `statsmodels`, `yfinance`
- `cvxpy`/`cvxopt` optional (fallback to `scipy.optimize`)
- Data cached in `data/` (gitignored except pinned vintages 2026-10-11, 2026-10-12)

---

*This handoff was created automatically at session start. Update as needed before session end.*