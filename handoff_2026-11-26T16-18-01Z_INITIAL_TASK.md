# Handoff: Next Agentic Work Session

**Timestamp**: 2026-11-26T16:18:01Z
**Session**: Quantitative Trading Research — Verification & Reproducibility
**Branch / HEAD**: `main` @ `c80e2904` ("chore(kilo): checkpoint agent session")

---

## Initial Task Message (read first)

You are resuming an independent, reproducible quantitative-strategy research repo
(2014–2026 US equities, futures, macro). **Research phase is COMPLETE (E001–E043)**;
surviving validated strategies are recorded in `ledger/RESEARCH_LEDGER.md`. Your job
is to **preserve the verified baseline and only add pre-registered work**, never to
silently mutate canonical artifacts.

**Do this, in order:**
1. Run `SEED=42 make check` first. It must PASS (convention robustness + template +
   golden-integrity guards). If it reports a golden mismatch, **stop and restore**
   (`SEED=42 python3 run_all_verification.py --restore-only`) before anything else —
   do not commit verification output over the baseline.
2. Confirm the working tree is clean apart from ignored build artifacts
   (`src/__pycache__/*.pyc` is expected noise; `experiments/` must be untouched).
3. Only then pick an objective from the entry points below.

Golden rule: `experiments/*.json` are the authoritative record. Re-pin a golden
(`scripts/check_golden_baseline.py --update`, `scripts/check_data_coverage.py --update`)
**only** for a deliberate, ledger-recorded code/data change — never as a side effect
of running verification.

---

## Project State Summary

**Research Phase**: COMPLETE (E001–E043 executed)
**Surviving Strategies**: `ledger/RESEARCH_LEDGER.md`
**Verification Suite**: all tiers operational (`check`, `verify-quick`, `verify-extended`, `verify-full`)

### Key Artifacts (Canonical Baselines)
- `experiments/*.json` — committed golden outputs (never modified by verification)
- `ledger/golden_baseline.json` — SHA-256 fingerprints of all golden artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of pinned data caches
- `data/vintages.json` — 2026-10-12 vintage (primary)
- `data/fundamentals_vintages.json` — E029 fundamentals snapshot (2026-10-20)

### Verification Commands (SEED=42 always)
```bash
make check            # fast convention + integrity guards (~seconds)
make verify-quick     # ~8 min, 8 drivers + batch + validate + E042 n_sim=2
make verify-extended  # ~21 min, +18 committed drivers, structural match
make verify-full      # ~15 min, E042 n_sim=50 + 96-config sensitivity grid
```

---

## Current Status (as of this handoff)

### Last Verified
- `make check` — PASS (convention robustness + template validation)
- `make verify-quick` — PASS (8 drivers reproduce)
- `make verify-extended` — PASS (26 drivers reproduce, 0 differences at 2026-11-23T05:17Z)
- `make verify-full` — PASS (E042 n_sim=50 + 96-config grid)

### Critical Invariants (Enforced)
1. **Golden integrity**: `scripts/check_goldens_clean.py` + `scripts/check_golden_baseline.py` in `check.sh`
2. **Cache coverage**: `scripts/check_data_coverage.py` — every `data.download()` call site must have a pinned cache
3. **Optimizer determinism**: `src/portfolio_opt.py` validates on constraints, not solver exit status (ledger E049)
4. **Exact tangency solver**: E050 fix (commit `72dc947`) — active-set enumeration, bit-reproducible

### Known Drift (Closed)
- E041/E042 ill-conditioned QP drift → RESOLVED by E050 exact solver (0 differences since 2026-11-23)
- E029 offline-reproducible since 2026-10-20 (fundamentals pinned)
- E030 offline-reproducible since 2026-10-20 (16-ETF panel committed)

---

## Next Session: Suggested Entry Points

### If Continuing Verification
```bash
SEED=42 make check          # sanity
SEED=42 make verify-full    # full regression if time permits
```

### If Investigating a New Strategy
1. Read `ledger/RESEARCH_LEDGER.md` for surviving strategies and rejection rationale.
2. Pre-register the experiment: falsification expectations + sensitivity grid, in the driver docstring and its `pre_registered` JSON block.
3. Add `experiments/run_eXXX.py` following existing driver patterns.
4. Run verification to establish a new golden; record the change in the ledger before re-pinning.

### If Debugging Reproducibility
- `scripts/check_goldens_clean.py` — working-tree vs HEAD diffs
- `scripts/check_golden_baseline.py` — committed baseline vs pinned SHA-256 diffs
- `scripts/check_data_coverage.py` — missing cache entries
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only`

---

## Environment
- Python 3, deps in `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- Optional: cvxpy/cvxopt (optimizer falls back to scipy)
- Offline mode: `QUANT_RESEARCH_OFFLINE=1` (used by the verification suite)

---

**Next agent**: Start with `SEED=42 make check` to confirm baseline integrity, then proceed per objective. Do not commit until `check` is green and `experiments/` is unchanged.