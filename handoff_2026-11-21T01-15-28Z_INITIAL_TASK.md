# Handoff — Agentic Work Session

**Timestamp:** 2026-11-21T01:15:53Z
**Session ID:** (auto-generated)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

---

## Quick Reference Commands

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

## Key Files & Locations

| Category | Path |
|----------|------|
| Experiment drivers | `experiments/run_e*.py` |
| Golden artifacts (canonical) | `experiments/*.json` |
| Research ledger | `ledger/RESEARCH_LEDGER.md` |
| Golden baseline pins | `ledger/golden_baseline.json` |
| Data baseline pins | `ledger/data_baseline.json` |
| Verification suite | `run_all_verification.py` |
| Check scripts | `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py` |
| Core source | `src/` |
| Cached data (gitignored) | `data/` |

---

## Critical Integrity Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.

2. **Golden baseline is authoritative** — `ledger/golden_baseline.json` pins SHA-256 of every artifact under `experiments/`. `scripts/check_golden_baseline.py` enforces this. Do not re-pin as side effect of verification.

3. **Cache coverage is invariant** — every `data.download()` call site must have a committed, pinned cache file. Use `scripts/check_data_coverage.py --update` to add new inputs.

4. **E029, E030 are offline-reproducible** (since 2026-10-20, ledger E045/E048) — their data is pinned in `data/fundamentals/` and committed panel respectively.

5. **E041 drifts** — 133 numeric differences (1-ulp QP sensitivity), 3 structural differences fixed. Do not re-pin to silence — see ledger open item.

---

## Current State

- Research phase complete (E001–E043)
- Verification suite operational
- No active work in progress
- Ready for next task

---

## Suggested Next Steps

- Run `make check` to validate current state
- Run `make verify-quick` for fast verification
- Consult `ledger/RESEARCH_LEDGER.md` for strategy dispositions
- Any new experiment requires pre-registration with gates/falsification expectations

---

*This handoff was created automatically at session start. Update as work progresses.*