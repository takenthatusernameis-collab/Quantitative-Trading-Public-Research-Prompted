# Handoff — Agentic Work Session

**Timestamp:** 2026-11-26T07:08:26Z
**Session ID:** (auto-generated)
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## Project Context

**Quantitative Trading Research Repository** — Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.

- **Research Phase:** Complete (E001–E043)
- **Surviving Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Canonical Artifacts:** `experiments/*.json` (committed goldens)

---

## Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `SEED=42 bash scripts/check.sh` | Fast convention-robustness check (~seconds) |
| `SEED=42 python3 run_all_verification.py` | Quick full verification (~8 min) |
| `SEED=42 python3 run_all_verification.py --extended` | Extended verification (~21 min) |
| `SEED=42 python3 run_all_verification.py --full` | Full verification (~15 min, n_sim=50) |
| `SEED=42 python3 run_all_verification.py --restore-only` | Recover golden artifacts after interrupted run |

---

## Critical Integrity Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. Use `--restore-only` if interrupted.
2. **Golden baseline pinned in `ledger/golden_baseline.json`** — do not re-pin without ledger entry.
3. **Data cache coverage enforced** — `scripts/check_data_coverage.py` validates all download call sites.
4. **Convention:** Close-to-close primary (v1.2.3), overnight decomposition reported alongside.

---

## Current State

- No active verification run detected
- Working tree clean (assuming no uncommitted changes)
- Ready for next task

---

## Suggested Next Steps

- Run `SEED=42 bash scripts/check.sh` to verify environment health
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
- Check `experiments/` for available drivers
- Consider running `verify-quick` if changes were made

---

*This handoff was created automatically at session start. Update as work progresses.*