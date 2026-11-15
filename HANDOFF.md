# Handoff — Agentic Work Session

**Timestamp:** 2026-11-15T18:00:25Z
**Session ID:** (auto-generated)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Context

**Quantitative Trading Public Research** — Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates.

**Research phase:** Complete (E001–E043)
**Surviving validated strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

---

## Quick Start Commands

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

## Critical Integrity Notes

1. **Golden files** (`experiments/*.json`) are canonical artifacts. Verification overwrites them temporarily and restores — **never leave a verification run half-finished**.

2. **Recovery:** If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Baseline pinning:** `ledger/golden_baseline.json` pins SHA-256 of every tracked artifact. Never re-pin as side effect of verification — see AGENTS.md for re-pin protocol.

4. **Data cache coverage:** Enforced invariant (ledger E048). All `data.download()` calls must have committed, SHA-256-pinned cache files. Add inputs by committing file + `python3 scripts/check_data_coverage.py --update`.

5. **Optimizer determinism (ledger E049):** SLSQP status 8 is valid at constrained optimum. Tangency QP remains ill-conditioned — E041/E042 grid artifacts drift by 29-133 differences. **Do not re-pin to silence.**

---

## Current State

- Research phase complete (E001–E043)
- Ledger documents surviving strategies in `ledger/RESEARCH_LEDGER.md`
- All verification commands available via `make` or direct python scripts
- CI gate template at `.github/workflow-templates/verification-gate.yml` (maintainer must create actual workflow)

---

## Next Steps / Suggested Work

- [ ] Run `make check` to verify current state
- [ ] Run `make verify-quick` for fast verification
- [ ] Review `ledger/RESEARCH_LEDGER.md` for validated strategies
- [ ] Consider extending research with new pre-registered experiments (E044+)

---

*This handoff was created automatically at session start. Update as work progresses.*