# Agentic Work Session Handoff

**Timestamp**: 2026-11-19T00:40:39Z
**Session ID**: Initial handoff for next agentic session
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status Summary

**Research Phase**: Complete (E001–E043)
**Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
**Verification Suite**: Operational with multiple tiers (check, verify-quick, verify-extended, verify-full)

---

## Key Verification Commands

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

---

## Critical Integrity Notes (READ BEFORE RUNNING)

1. **Golden Artifacts**: `experiments/*.json` are canonical research artifacts. The verification suite backs them up before re-running and restores them afterward.

2. **Never Leave Verification Half-Finished**: A run that is killed (SIGKILL/OOM/session timeout) leaves a recoverable snapshot in `.verify_snapshot/` with an `ACTIVE.json` marker. Recovery: `SEED=42 python3 run_all_verification.py --restore-only`

3. **Baseline Protection**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` (both in `scripts/check.sh`) guard against accidental baseline replacement. If `check.sh` reports a golden mismatch, fix it **before** committing.

4. **Data Cache Coverage**: Enforced invariant since 2026-10-20 (ledger E048). `scripts/check_data_coverage.py` requires every `data.download()` call site to have a committed, SHA-256-pinned cache file. Unpinned inputs fail hard under `QUANT_RESEARCH_OFFLINE=1`.

5. **Optimizer Determinism**: `src/portfolio_opt.py` validates solver answers on constraints, not exit status. Tangency QP remains ill-conditioned — 1-ulp perturbations move `min_var` answers by ~1e-05. Do **not** re-pin E041/E042 grid artifacts to silence drift.

---

## Next Session Suggested Starting Points

1. **Run `make check`** to verify convention robustness and golden baseline integrity
2. **Run `make verify-quick`** for full quick verification suite
3. **Review `ledger/RESEARCH_LEDGER.md`** for surviving strategies and open items (E049 optimizer determinism, E041 drift)
4. **Check `scripts/check_data_coverage.py`** output if adding new data inputs

---

**Handoff Complete** — Next agentic session can resume from this documented state.
