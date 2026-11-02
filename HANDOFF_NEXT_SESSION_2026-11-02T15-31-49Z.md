# DURABLE HANDOFF - Next Agentic Work Session

**Timestamp:** 2026-11-02T16:36:03Z
**Repository:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Branch:** `main` (check with `git branch --show-current`)
**HEAD:** Check with `git rev-parse HEAD`

---

## INITIAL TASK (Clear & Actionable)

**Goal:** Verify baseline integrity and establish a clean working state before starting any new work.

The repository is in a research-complete state (E001–E043). All surviving strategies are documented in `ledger/RESEARCH_LEDGER.md`. The golden artifacts in `experiments/` are the authoritative record and must remain clean. Your first priority is to confirm this state and surface any drift/blockers.

### Step 1: Verify Baseline Integrity (Required)
Run the full convention/golden/data integrity checks before making changes:

```bash
SEED=42 bash scripts/check.sh
```

This runs: py_compile, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, convention robustness, and the portfolio opt unit tests.

### Step 2: If Anything Fails (Recovery)
If `check.sh` reports golden/data mismatches or a stale snapshot:

```bash
# Recover goldens from HEAD (or the pinned baseline if HEAD was contaminated)
SEED=42 python3 run_all_verification.py --restore-only

# Re-verify after recovery
SEED=42 bash scripts/check.sh
```

**Do not re-pin goldens as a side effect of running verification.** The ledger's stance is the committed baseline is authoritative. Only re-pin if explicitly instructed and with justification documented.

---

## Context For The Next Session

- **Research phase:** Complete (E001–E043). See `ledger/RESEARCH_LEDGER.md` for dispositions (REJECTED/PARTIAL/accepted) and promotion gates.
- **Golden files:** `experiments/*.json` are committed and must match `ledger/golden_baseline.json` (SHA-256). `run_all_verification.py` backs up/restores them - never leave a verification run half-finished.
- **Data integrity:** All cache inputs are pinned/covered by `ledger/data_baseline.json`. `QUANT_RESEARCH_OFFLINE=1` is used by verification; missing caches must fail, not download.
- **Known open item:** E041 still shows numeric drift (133 numeric diffs) due to ill-conditioned QP in `src/portfolio_opt.py`. The structural issue is fixed and gates are unchanged (REJECTED 3/5). **Do not re-pin to silence this drift.** See ledger E049.
- **E029/E030:** Now offline-reproducible due to pinned fundamentals/panels. See ledger notes.

---

## Suggested Follow-Up Tasks (After Clean Baseline)

1. **Review open items** - Read `ledger/RESEARCH_LEDGER.md` for any items marked open/investigation and confirm their current status.
2. **Decide direction** - Either (a) document/close the E041 drift investigation with evidence, (b) harden tests around the optimizer determinism, or (c) start a new pre-registered experiment only if explicitly requested. The default is to not start new experiments without clear justification.
3. **CI note** - The intended GitHub workflow cannot be auto-created by agents; see `VERIFICATION_GATE_TEMPLATE.md` if CI hardening is requested.

---

## Key Files To Read First
- `AGENTS.md` - Commands, conventions, baseline integrity rules
- `ledger/RESEARCH_LEDGER.md` - Authoritative research history and dispositions
- `ledger/golden_baseline.json` - Pinned SHA-256s for golden artifacts
- `ledger/data_baseline.json` - Pinned data cache coverage
- `run_all_verification.py` - Verification orchestration and restore logic
- `scripts/check.sh` - Primary integrity gate

---

## Quick Verification Commands
```bash
# Integrity
SEED=42 bash scripts/check.sh

# Full verification (slow, only if needed)
SEED=42 python3 run_all_verification.py

# Convention robustness only (fast)
SEED=42 python3 verify_convention_robustness.py
```
