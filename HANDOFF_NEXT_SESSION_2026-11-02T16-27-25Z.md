# HANDOFF

**Timestamp (UTC):** 2026-11-02T16:27:25Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**State:** Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

---

## Context (carry-forward)

- **Canonical baselines:** `experiments/*.json` are authoritative goldens. Protected by `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py`. Never leave a verification run half-finished. Backups live in `.verify_snapshot/` (gitignored) with `ACTIVE.json` tracking ownership.
- **Verification:** `scripts/check.sh` runs conventions, golden cleanliness, golden baseline pinning, and tests. `run_all_verification.py` backs up/restores goldens automatically.
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages). `data/vintages.json` pins 2026-10-12; 2026-10-11 committed for specific experiments. Fundamentals for E029 pinned in `data/fundamentals/`. `scripts/check_data_coverage.py` enforces cache coverage.
- **Known issues:** Optimizer determinism (ledger E049) — tangency QP ill-conditioned (1-ulp sensitivity) causing numeric drift in E041/E042 grids. **Do not re-pin goldens to silence known numeric drift.** E041 structural diffs fixed; remaining ~133 numeric diffs are expected. E029/E030 are offline-reproducible.

---

## Initial Task for Next Session (Priority Order)

1. **[ ] Verify repo integrity (required before any changes)**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   If it reports a golden mismatch or stale snapshot, recover:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   # or: git checkout -- experiments/
   # or checkout the pinned commit from ledger/golden_baseline.json
   ```

2. **[ ] Review open items in the ledger**
   Read `ledger/RESEARCH_LEDGER.md` and identify the highest-priority open item. Pay particular attention to:
   - E041/E042 numeric drift (ill-conditioned QP) — open; do not re-pin
   - Any entries added since the previous handoff
   - Promotion gates/status for surviving strategies

3. **[ ] Execute the next concrete action from the ledger**
   Based on (2), proceed with that action. If there is no explicit next task, confirm research-phase state is intact and report status. **Do not** re-pin goldens as a side effect of verification or to silence known numeric drift.

---

## Quick Reference

| Action | Command |
| --- | --- |
| Fast check (goldens + conventions + tests) | `SEED=42 bash scripts/check.sh` |
| Quick full verification (~8 min) | `SEED=42 python3 run_all_verification.py` |
| Extended verification (~21 min) | `SEED=42 python3 run_all_verification.py --extended` |
| Full verification (~15 min, heavy) | `SEED=42 python3 run_all_verification.py --full` |
| Recover goldens after interruption | `SEED=42 python3 run_all_verification.py --restore-only` |
| Convention robustness only | `SEED=42 python3 verify_convention_robustness.py` |
| Check data cache coverage | `python3 scripts/check_data_coverage.py` |
| Check golden baseline pinning | `python3 scripts/check_golden_baseline.py` |

---

## Guardrails

- **Never commit verification output.** If a run is interrupted, restore goldens before committing.
- **Never re-pin to silence known drift.** Re-pinning requires explicit justification and `scripts/check_golden_baseline.py --update`. Committed goldens are authoritative.
- **Data must be cached/pinned.** Adding new data requires committing the file and re-pinning via `scripts/check_data_coverage.py --update`.
- **Respect pre-registration.** Goalposts never moved post-hoc. Sensitivity grids reported, not gated.
- **Offline safety.** Suite runs with `QUANT_RESEARCH_OFFLINE=1` — missing cache entries fail hard.
