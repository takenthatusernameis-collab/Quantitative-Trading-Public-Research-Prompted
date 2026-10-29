# HANDOFF — Next Agentic Work Session
**Timestamp (UTC):** 2026-10-29T21:32:29Z
**From:** Kilo (current session)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD context:** Research phase complete (E001–E043)

---

## Current State Summary
- **Research complete:** E001–E043 finished. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Golden baseline is authoritative:** `experiments/*.json` are canonical. The verification suite backs up/restores them; never leave a run half-finished. Guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py` (see AGENTS.md).
- **Recent known items (from AGENTS.md):**
  - **E041 drift:** Optimizer sensitivity remains (ill-conditioned tangency QP). Numeric diffs reduced but still > 1e-4; do **not** re-pin to silence. Structural diffs fixed. See ledger E049.
  - **E029/E030:** Data pinned (fundamentals snapshot, 16-ETF panel) for offline reproducibility.
  - **Optimizer determinism:** SLSQP status 8 handled correctly (validation on constraints). Covered by `tests/test_portfolio_opt.py`.

---

## INITIAL TASK (Clear & Actionable)

**Goal:** Establish a clean baseline and decide next action from the ledger.

**Steps (do in order):**
1. **Verify repo integrity first (fast):**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - Must pass: py_compile, convention robustness, golden-clean, golden-baseline, data coverage, optimizer tests. If it reports a golden mismatch, restore before proceeding (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` as appropriate).

2. **Read the source of truth:**
   - `ledger/RESEARCH_LEDGER.md` — focus on open items (especially E041), any "open"/"partial" entries, and promotion gates.
   - `ledger/golden_baseline.json` and `ledger/data_baseline.json` — confirm fingerprints.

3. **Propose/execute the next concrete action:**
   Based on ledger state, pick **one** of:
   - **If E041 needs attention:** Investigate optimizer sensitivity further (document bounded drift, consider alternative solvers/tolerances, add regression guard) without re-pinning goldens.
   - **If promoting a strategy:** Follow pre-registration + multiple-testing discipline (sensitivity grid reported-not-gated; confirmatory run with full placebo before promotion).
   - **If extending research:** Only start a new pre-registered experiment if ledger shows a clear gap; update ledger and add driver + golden only per conventions.

**Success criteria:** `scripts/check.sh` passes on clean baseline, ledger read completed, and a short plan recorded (or work started) with no changes to `experiments/` goldens unless explicitly justified and re-pinned via the designated script.

---

## Quick Commands
```bash
# Fast check
SEED=42 bash scripts/check.sh

# Quick verification (restores goldens)
SEED=42 python3 run_all_verification.py

# Extended/full if needed
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full

# Recovery
SEED=42 python3 run_all_verification.py --restore-only
```

---

## Key Files to Read First
- `AGENTS.md` (commands, guards, conventions)
- `ledger/RESEARCH_LEDGER.md`
- `scripts/check.sh`, `run_all_verification.py`
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py` (if touching optimizer)

**Note:** Do not commit verification artifacts. Follow all baseline integrity rules strictly.
