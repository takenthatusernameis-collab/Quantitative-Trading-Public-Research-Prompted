# Agentic Work Session Handoff

**Timestamp**: 2026-11-14T23:32:15Z
**Session ID**: Initial handoff created by Kilo
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

---

## Project Status Summary

**Research Phase**: COMPLETE (Experiments E001–E043 finished)
**Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
**Current Baseline**: Golden artifacts in `experiments/*.json` (canonical, committed)

---

## Key Verification Commands

| Command | Duration | Purpose |
|---------|----------|---------|
| `make check` / `SEED=42 bash scripts/check.sh` | ~seconds | Convention robustness + template validation (offline) |
| `make verify-quick` / `SEED=42 python3 run_all_verification.py` | ~8 min | 8 experiment drivers + batch_run + validate + E042 n_sim=2 |
| `make verify-extended` / `SEED=42 python3 run_all_verification.py --extended` | ~21 min | Quick + 18 more drivers, structural match |
| `make verify-full` / `SEED=42 python3 run_all_verification.py --full` | ~15 min | E042 n_sim=50 + 96-config sensitivity grid |

---

## Critical Integrity Notes (Read Before Running)

1. **Golden files are canonical** — `experiments/*.json` are committed artifacts. Verification overwrites them temporarily and restores after. **Never leave a verification run half-finished.**

2. **Recovery if interrupted**:
   `SEED=42 python3 run_all_verification.py --restore-only`
   or `git checkout -- experiments/`

3. **Baseline protection**:
   - `scripts/check_goldens_clean.py` compares working tree vs HEAD
   - `scripts/check_golden_baseline.py` compares vs pinned SHA-256 in `ledger/golden_baseline.json`
   - Never re-pin as side effect of verification — committed golden is authoritative

4. **Data cache invariants** (enforced 2026-10-20):
   - `scripts/check_data_coverage.py` validates every `data.download()` call site
   - All cache files must exist, be git-tracked, match `ledger/data_baseline.json`
   - Verification runs with `QUANT_RESEARCH_OFFLINE=1` — missing cache = hard failure

5. **Known floating-point drift** (acceptable, not structural):
   - E011, E030, E041 show small numeric drift (1e-4 tolerance)
   - E041: 133 numeric diffs from ill-conditioned QP (optimizer determinism fixed, but QP remains sensitive)
   - **Do not re-pin to silence drift** — see ledger open items

---

## Reproducibility Requirements

- **Seed**: Always `SEED=42` (walk-forward + placebo RNG)
- **Data vintage**: 2026-10-12 pinned in `data/vintages.json`; 2026-10-11 committed for E026/E028/E029/E030/E034/E036/E037
- **E029 fundamentals**: Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` — fully offline reproducible
- **Dependencies**: `pip install -r requirements.txt` (cvxpy/cvxopt optional; falls back to scipy)

---

## Next Session Suggested Starting Points

1. **Run quick verification** to confirm baseline integrity:
   `SEED=42 python3 run_all_verification.py`

2. **Check ledger for open items**:
   `cat ledger/RESEARCH_LEDGER.md` — look for E049 (optimizer determinism), E041 drift, E030/E029 re-pin notes

3. **If adding new experiment**:
   - Pre-register with gates/falsification expectations in driver docstring
   - Add `data.download()` call sites → run `scripts/check_data_coverage.py --update` to pin
   - Commit golden artifact to `experiments/`

---

## Files to Review First

- `ledger/RESEARCH_LEDGER.md` — surviving strategies, dispositions, open items
- `ledger/golden_baseline.json` — SHA-256 pins for all experiment artifacts
- `ledger/data_baseline.json` — SHA-256 pins for all data cache files
- `scripts/check.sh` — full pre-commit validation pipeline
- `AGENTS.md` — this file's conventions and commands

---

**End of Handoff** — Next agent should verify baseline integrity before proceeding.