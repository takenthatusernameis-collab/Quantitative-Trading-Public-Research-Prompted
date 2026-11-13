# Agentic Work Session Handoff

**Timestamp:** 2026-11-13T00:05:08Z
**Session ID:** Current session
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status

**Research Phase:** Complete (E001–E043)
**Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Baseline Integrity:** Golden artifacts in `experiments/*.json` are canonical and pinned in `ledger/golden_baseline.json`

---

## Key Verification Commands

```bash
# Fast convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min, structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, E042 n_sim=50 + 96-config sensitivity)
SEED=42 python3 run_all_verification.py --full
```

---

## Critical Baseline Rules

1. **Never leave verification half-finished** — `experiments/*.json` are overwritten during verification and restored afterward
2. **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Golden baseline pinned:** Compare with `ledger/golden_baseline.json` SHA-256 fingerprints via `scripts/check_golden_baseline.py`
4. **Data cache coverage enforced:** `scripts/check_data_coverage.py` validates all `data.download()` call sites
5. **Offline reproducibility:** Set `QUANT_RESEARCH_OFFLINE=1` for verification runs

---

## Current State

- No active verification run in progress (no `.verify_snapshot/ACTIVE.json`)
- All golden artifacts should match HEAD
- Data vintages pinned: 2026-10-12 (`data/vintages.json`) and 2026-10-11 (committed for E026/E028/E029/E030/E034/E036/E037)
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- E030 16-ETF panel committed (offline-reproducible since 2026-10-20)

---

## Known Drift (Extended Verification)

- **E030:** 28 numeric diffs on near-zero quantities (reproduces with 0 diffs since 2026-10-20 after panel pinning)
- **E041:** 133 numeric diffs (1-ulp QP sensitivity, ill-conditioned tangency portfolio), 3 structural diffs resolved — **do not re-pin** (open ledger item E049)

---

## Next Session Guidance

1. Run `SEED=42 bash scripts/check.sh` first to verify baseline integrity
2. Use `make verify-quick` for standard verification
3. Check `ledger/RESEARCH_LEDGER.md` for surviving validated strategies
4. Any new experiments must follow pre-registration protocol (gates, falsification expectations, sensitivity grids)
5. Negative results (REJECTED/PARTIAL) recorded honestly with evidence

---

*This handoff was created automatically at session start for durability across agentic work sessions.*