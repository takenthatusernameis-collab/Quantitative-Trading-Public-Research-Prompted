# Durable Handoff — Next Agentic Work Session
**Timestamp:** 2026-10-30T13-27-28Z (UTC)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `c38b22f` (HEAD)
**Working tree:** clean of source/data changes; only `__pycache__/*.pyc` modified (build artifacts).
**Snapshot state:** no `.verify_snapshot/ACTIVE.json` visible — run guards before verifying.

## Status
Research phase complete (E001–E043). Market-neutral total portfolio closed (E042 PARTIAL 4/5, E042b REJECTED 4/5).
`src/portfolio_opt.py` solver-status gating fixed (E049); `tests/test_portfolio_opt.py` added as first-class `scripts/check.sh` step.
Known drift: E041 shows numeric drift from ill-conditioned tangency QP sensitivity despite fixed gating — do **not** silence by re-pinning (see ledger E049).

## Clear initial task (start here)
**Primary objective:** Establish/confirm a clean verification baseline with integrity guards green before any new work.

### Concrete steps (in order)
1. **Inspect state**
   ```bash
   git log -1 --oneline
   git status --short
   ```

2. **Clean build artifacts (optional)**
   ```bash
   find . -name "*.pyc" -path "*/__pycache__/*" -delete
   ```

3. **Integrity guards**
   ```bash
   SEED=42 bash scripts/check.sh  # or make check
   ```
   If pending snapshot/golden mismatch reported, recover first:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```

4. **Quick verification**
   ```bash
   SEED=42 python3 run_all_verification.py  # verify-quick
   ```
   Ensure completion with goldens restored. Do **not** commit verification outputs.

5. **Review open items**
   - Read `ledger/RESEARCH_LEDGER.md` (focus E041/E048/E049)
   - Read `ledger/golden_baseline.json`, `ledger/data_baseline.json`
   - Note extended drift expected for E041 (ill-conditioned QP); do not re-pin.

### Success criteria
- `make check` passes
- `verify-quick` passes with goldens intact (`experiments/` unchanged vs HEAD)
- No stray source/data changes before starting new work

## Key artifacts
- `AGENTS.md` — commands, baseline integrity, reproducibility
- `ledger/RESEARCH_LEDGER.md` — pre-registered goals/gates/results/open items
- `run_all_verification.py`, `scripts/check_{goldens_clean,golden_baseline,data_coverage}.py`
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`

## Guardrails
- Always use `SEED=42`. Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`).
- Never leave `run_all_verification.py` half-finished.
- Never re-pin goldens as side effect of verification; use `scripts/check_golden_baseline.py --update` only with ledger justification and diff.
- E041 numeric drift expected due to ill-conditioned QP — do not "fix" by re-pinning.
- Any new data input must be committed and pinned via `scripts/check_data_coverage.py --update`.

## Quick reference
```bash
# Integrity
SEED=42 make check

# Verify
SEED=42 make verify-quick
SEED=42 make verify-extended
SEED=42 make verify-full

# Recover
SEED=42 python3 run_all_verification.py --restore-only

# Clean
find . -name "*.pyc" -path "*/__pycache__/*" -delete
```

**Handoff outcome:** Once guards + verify-quick are green with goldens intact and only `__pycache__` artifacts present, baseline is clean and next session may proceed.
