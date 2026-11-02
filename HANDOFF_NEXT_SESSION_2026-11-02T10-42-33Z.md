# HANDOFF

**Timestamp (UTC):** 2026-11-02T10:47:43Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**State:** Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

---

## Context

- **Canonical baselines:** `experiments/*.json` are the authoritative golden artifacts. They are protected by `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py`. A verification run must never be left half-finished. Backups live in `.verify_snapshot/` (gitignored) with `ACTIVE.json` tracking ownership.
- **Verification guards:** `scripts/check.sh` runs convention checks, golden cleanliness, golden baseline pinning, and tests. `run_all_verification.py` backs up/restores goldens automatically.
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages). `data/vintages.json` pins 2026-10-12, and 2026-10-11 is committed for specific experiments. Fundamentals for E029 are pinned in `data/fundamentals/`. `scripts/check_data_coverage.py` enforces cache coverage — missing/pinned-mismatched inputs fail hard.
- **Reproducibility notes:** `SEED=42` always. Optimizer determinism issue (ledger E049): tangency QP is ill-conditioned (1-ulp sensitivity) causing numeric drift in E041/E042 grids. Do **not** re-pin goldens to silence this drift. E041's structural differences are fixed, remaining 133 numeric diffs are expected sensitivity. E029/E030 are now offline-reproducible.

---

## Initial Task for Next Session (Priority Order)

1. **[ ] Verify repo integrity**
   Run the fast convention+golden check before making any changes:
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   If it reports a golden mismatch or stale snapshot, recover per `AGENTS.md`:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   # or git checkout -- experiments/ (if HEAD is correct)
   # or checkout the pinned commit from ledger/golden_baseline.json
   ```

2. **[ ] Review open items in the ledger**
   Read `ledger/RESEARCH_LEDGER.md` to identify the current highest-priority open item. Pay particular attention to:
   - E041/E042 numeric drift (ill-conditioned QP) — open item, do not re-pin
   - Any new entries since last session
   - Promotion gates for surviving strategies

3. **[ ] Decide and execute next action**
   Based on the ledger, proceed with the next concrete action. If the ledger has no explicit next task, confirm the research phase state is intact and report status. **Do not** re-pin goldens as a side effect of verification or to silence known numeric drift.

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
- **Never re-pin to silence known drift.** Re-pinning requires explicit justification and `scripts/check_golden_baseline.py --update`. The ledger's disposition is: committed goldens are authoritative.
- **Data must be cached/pinned.** Adding new data requires committing the file and re-pinning via `scripts/check_data_coverage.py --update`.
- **Respect pre-registration.** Goalposts are never moved post-hoc. Sensitivity grids are reported, not gated.
- **Offline safety.** The suite runs with `QUANT_RESEARCH_OFFLINE=1` — missing cache entries will fail hard.
