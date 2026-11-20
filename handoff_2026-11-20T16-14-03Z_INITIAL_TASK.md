# Handoff — Agentic Work Session

**Timestamp:** 2026-11-20T16:14:03Z
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Research Phase:** Complete (E001–E043) — see `ledger/RESEARCH_LEDGER.md`

---

## Initial Task for Next Session

Run the fast convention check to confirm the baseline is intact before any other work:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If `scripts/check.sh` reports a golden mismatch under `experiments/`, fix it before committing — a checkpoint commit that captures verification output silently replaces the canonical baseline (see `AGENTS.md` "Baseline Integrity"). Recover with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.

## Verification Suite (use only if needed)

- Quick (~8 min): `SEED=42 python3 run_all_verification.py` / `make verify-quick`
- Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended` / `make verify-extended`
- Full (~15 min): `SEED=42 python3 run_all_verification.py --full` / `make verify-full`
- Restore artifacts after an interrupted run: `SEED=42 python3 run_all_verification.py --restore-only`

Never leave a verification run half-finished: it overwrites `experiments/*.json` and restores on completion.

## Critical Integrity Notes

1. `experiments/*.json` are the canonical research artifacts; `ledger/golden_baseline.json` pins their SHA-256 fingerprints. Never re-pin as a side effect of verification.
2. `scripts/check_data_coverage.py` (ledger E048): every `data.download()` call site needs a committed, SHA-256-pinned cache file — missing cache = live network download, which fails under `QUANT_RESEARCH_OFFLINE=1`.
3. Optimizer determinism (ledger E049): `src/portfolio_opt.py` validates on constraints, not solver exit status. E041/E042 grid artifacts drift 29–133 differences (1-ulp QP sensitivity) — do not re-pin to silence.

## Open Items (from Ledger)

- E041 drift: 133 numeric differences remain — decision REJECTED 3/5 unchanged
- E042 min-var confirmatory: PARTIAL
- No surviving strategies promoted beyond research phase

## Key Files

- `AGENTS.md` — project commands & conventions (read before running the suite)
- `ledger/RESEARCH_LEDGER.md` — experiment dispositions & open items
- `src/portfolio_opt.py` — optimizer determinism rule
- `scripts/check_goldens_clean.py` / `scripts/check_golden_baseline.py` — golden guards
- `scripts/check_data_coverage.py` — data cache coverage invariant
