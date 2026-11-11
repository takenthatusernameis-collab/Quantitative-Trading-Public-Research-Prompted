# Agentic Work Session Handoff

**Timestamp:** 2026-11-11T06:28:59Z
**Session ID:** (new session)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Context

**Quantitative Trading Research Repository** — Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

### Key Verification Commands
```bash
# Fast convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

### Critical Baseline Integrity Rules
- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden artifacts pinned in `ledger/golden_baseline.json` — never re-pin as side effect of verification
- Cache coverage enforced: `scripts/check_data_coverage.py` validates all data inputs

### Current State
- Research phase: **COMPLETE** (E001–E043)
- Last verified: Check `ledger/RESEARCH_LEDGER.md` for surviving strategies
- Data vintage: 2026-10-12 (pinned in `data/vintages.json`), 2026-10-11 (committed for specific experiments)
- E029 fundamentals: Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

---

## Handoff Instructions for Next Session

1. **Run `scripts/check.sh` first** to verify baseline integrity before any work
2. **Check `ledger/RESEARCH_LEDGER.md`** for current strategy dispositions
3. **Use `SEED=42`** for all reproducibility
4. **Do not commit verification output** — restore goldens before committing
5. **Pre-register any new experiments** with gates/falsification expectations

---

## Available Skills
- `kilo-config` — Kilo configuration guidance

---

*This handoff was created automatically at session start. Update as work progresses.*