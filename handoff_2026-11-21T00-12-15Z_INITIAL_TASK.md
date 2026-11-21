# Agentic Work Session Handoff

**Timestamp**: 2026-11-21T00:12:15Z
**Session**: Initial handoff for next agentic work session

## Project State

**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Phase**: Research complete (E001–E043) — surviving strategies in `ledger/RESEARCH_LEDGER.md`

## Key Context for Next Session

### Verification Suite Status
- **Golden artifacts**: `experiments/*.json` are canonical baselines (pinned SHA-256 in `ledger/golden_baseline.json`)
- **Data vintage**: 2026-10-12 (prices, `data/vintages.json`) + 2026-10-11 (E026/E028/E029/E030/E034/E036/E037) + E029 fundamentals (`data/fundamentals_vintages.json`)
- **Critical rule**: Verification runs overwrite `experiments/` then restore — **never leave a run half-finished**

### Standard Commands
```bash
# Fast convention check (offline, seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min, 8 drivers + batch + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min, +18 drivers, structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py

# Recovery if verification interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

### Known Drift (Extended Verification)
- **E030**: 28 numeric diffs on near-zero quantities (fixed by pinning 16-ETF panel, ledger E048)
- **E041**: 133 numeric diffs (1-ulp QP sensitivity, ill-conditioned tangency) + 3 structural diffs resolved (ledger E049)
- **Do not re-pin** E041/E042 grid artifacts to silence drift — see ledger open items

### Optimizer Determinism (ledger E049)
- `src/portfolio_opt.py` validates on **problem constraints**, not solver exit status
- SLSQP status 8 ("Positive directional derivative") can occur at constrained optimum
- Tangency QP remains ill-conditioned: 1-ulp input perturbation → ~1e-05 min_var drift

### Data Coverage Invariant (ledger E048)
- `scripts/check_data_coverage.py` enforces: every `data.download()` call site → committed parquet + SHA-256 in `ledger/data_baseline.json`
- Verification runs with `QUANT_RESEARCH_OFFLINE=1` — missing cache = hard fail
- To add data input: commit file → `python3 scripts/check_data_coverage.py --update`

## Pre-registration Discipline
- Every driver has `pre_registered` JSON block + docstring with gates/falsification/sensitivity **before execution**
- Sensitivity grids: "reported, not gated" — config clearing gates needs dedicated confirmatory run + full placebo
- Negative results recorded honestly (REJECTED / PARTIAL) with evidence

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Run verification tier appropriate to goal (`verify-quick` / `verify-extended` / `verify-full`)
4. If modifying drivers/data: respect golden baseline — never re-pin without ledger entry

---

*This handoff is durable across sessions. Update it when project state changes materially.*
