# Handoff — Agentic Work Session

**Timestamp:** 2026-11-27T20:37:05Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

---

## Verification Commands (from AGENTS.md)

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

## Key Integrity Notes

- **Golden files**: `experiments/*.json` are canonical artifacts. Verification overwrites them temporarily and restores afterward.
- **Never leave a verification run half-finished** — use `--restore-only` to recover if interrupted.
- **Baseline pinned in `ledger/golden_baseline.json`** — do not re-pin without ledger entry.
- **Data cache coverage enforced** — all `data.download()` calls must have pinned SHA-256 in `ledger/data_baseline.json`.
- **Optimizer determinism** (ledger E049/E050): SLSQP status gating removed; exact active-set enumeration ensures bit-reproducibility.

---

## Next Session Suggestions

1. Run `make check` to verify baseline integrity before any changes
2. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
3. Check `scripts/check_golden_baseline.py` and `scripts/check_data_coverage.py` for current baseline status
4. Consider extended verification if making changes to experiment drivers

---

*This handoff was created automatically at session start. Update as needed during work.*