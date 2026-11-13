# Agentic Work Session Handoff

**Timestamp:** 2026-11-13T15:27:18Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status

**Research Phase:** Complete (E001–E043)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

## Quick Reference Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Critical Integrity Notes (from AGENTS.md)

1. **Golden Artifacts**: `experiments/*.json` are canonical baselines. Verification overwrites them temporarily and restores after — **never leave a verification run half-finished**.

2. **Recovery**: If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Cache Coverage**: Enforced invariant — `scripts/check_data_coverage.py` validates every `data.download()` call site resolves to a committed, SHA-256-pinned cache file.

4. **E041 Drift**: Known optimizer non-determinism (1-ulp QP sensitivity) — 133 numeric diffs remain. **Do not re-pin** — see ledger open item.

5. **E029/E030**: Now offline-reproducible since 2026-10-20 (pinned fundamentals/ETF panels).

---

## Next Session Suggested Starting Points

- [ ] Run `make check` to validate current state
- [ ] Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
- [ ] Consider next research direction (promotion gates, new pre-registrations, etc.)

---

*This handoff was created automatically for session continuity.*