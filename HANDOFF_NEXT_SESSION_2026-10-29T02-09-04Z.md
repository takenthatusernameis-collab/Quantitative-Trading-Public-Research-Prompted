# HANDOFF — Initial Task Message for Next Agentic Work Session

**Timestamp (UTC):** 2026-10-29T02:09:04Z
**Handoff ID:** handoff-20261029T020904Z
**From:** Current session (no new work performed; baseline verified, handoff written)
**To:** Next agentic work session

---

## Repository State (verified this session)

- **Project:** Quantitative-Trading-Public-Research-Prompted (US equities/futures/macro, 2014–2026)
- **Phase:** Research complete (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **HEAD:** `d5cf92a` chore(kilo): checkpoint agent session, branch `main`, up to date with `origin/main`.
- **Working tree:** Clean (only gitignored `__pycache__` artifacts). No tracked changes.
- **Snapshot:** `.verify_snapshot/` absent — no live verification run, nothing to recover.
- **Baseline integrity:** `SEED=42 bash scripts/check.sh` → ALL CHECKS PASSED. Golden cleanliness, data coverage, optimizer tests, convention robustness, template validation, and experiment-script imports all green.

---

## Initial Task (Clear & Actionable)

**Resume from a clean, verified baseline. Confirm state before starting new work.**

### Step 1 — Confirm baseline integrity (MUST pass first)
```bash
SEED=42 bash scripts/check.sh
```
If it fails: restore via `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`; never re-pin to silence.

### Step 2 — Quick verification (~8 min)
```bash
SEED=42 python3 run_all_verification.py   # or: make verify-quick
```

### Step 3 — Extended verification (optional, ~21 min)
```bash
SEED=42 python3 run_all_verification.py --extended
```
Expect known reporting-only drift; do NOT re-pin.

### Step 4 — Triage & report
- If clean: review open ledger items and propose next concrete work.
- If drift: investigate per AGENTS.md; do not re-pin goldens.

---

## Open Items (from `ledger/RESEARCH_LEDGER.md`)

1. **E049 residual:** tangency QP ill-conditioned — replace SLSQP with well-conditioned deterministic solver (exact active-set enumeration for N <= 5), then deliberately re-pin affected artifacts.
2. **E049 secondary defect (not fixed):** `y0 = w_feas / max(mu_s'w_feas, 1e-12)` (`src/portfolio_opt.py:253`) masks a negative denominator at the 2019-10-16 rebalance. Left for the same deliberate re-pin.
3. **Known reporting-only drift (do not re-pin):** E030 (near-zero quantities), E041 (~133 numeric diffs, 3 structural resolved). Decisions and gate flags unchanged.

---

## Guardrails

- Goldens authoritative; never let verification overwrite committed `experiments/*.json`.
- Pre-registration first for any new experiment.
- MHT: sensitivity grids reported, not gated; promotion needs confirmatory run with placebo.
- Offline discipline: prefer pinned data/vintages; suite runs `QUANT_RESEARCH_OFFLINE=1`.
- Optimizer rule: validate on problem constraints, not solver exit status.
- Do not create `.github/workflows/`; use template if needed.
- Only commit when explicitly requested; never commit verification output or corrupted goldens.

---

## Quick References

- Commands: `AGENTS.md`
- Ledger: `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- Extended: `SEED=42 python3 run_all_verification.py --extended`
- Full: `SEED=42 python3 run_all_verification.py --full`
- Convention: `SEED=42 python3 verify_convention_robustness.py`

---

## Handoff Metadata

- **Created:** 2026-10-29T02:09:04Z
- **Created by:** Current agentic session
- **Purpose:** Durable handoff with a clear, timestamped initial task for the next session
