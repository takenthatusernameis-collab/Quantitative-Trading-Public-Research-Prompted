# HANDOFF — Initial Task Message for Next Agentic Work Session

**Timestamp (UTC):** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Handoff ID:** handoff-$(date -u +%Y%m%dT%H%M%SZ)
**From:** Current session
**To:** Next agentic work session

---

## Repository State (verified this session)

- **Project:** Quantitative-Trading-Public-Research-Prompted (US equities/futures/macro, 2014–2026)
- **Phase:** Research complete (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **HEAD:** $(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted rev-parse --short HEAD) $(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted log -1 --format='%s')
- **Branch:** $(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted branch --show-current)
- **Working tree:** $(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted diff --quiet && git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted diff --cached --quiet && echo "Clean (no tracked changes)" || echo "Has changes")
- **Baseline integrity:** `SEED=42 bash scripts/check.sh` → **ALL CHECKS PASSED** (exit 0). Golden cleanliness, data coverage, optimizer tests, convention robustness, template validation, and all experiment-script imports all green.

---

## Initial Task (Clear & Actionable)

**Resume from a clean, verified baseline. Do not start new work without first confirming state.**

### Step 1 — Confirm baseline integrity (MUST pass first)
```bash
SEED=42 bash scripts/check.sh
```
If it fails:
- Stale snapshot → `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- `experiments/` differs from HEAD due to a captured run → restore to HEAD. If HEAD itself was incorrectly re-pinned, restore from the commit whose SHA-256 matches `ledger/golden_baseline.json`.
- Data coverage fails → **do not download**. Check `ledger/data_baseline.json`; commit missing pinned data before proceeding.

### Step 2 — Quick verification (confirm reproducibility)
```bash
SEED=42 python3 run_all_verification.py
# or: make verify-quick
```
Re-runs the 8 quick drivers (E012, E023, E024, E027, E035, E037, E039, E042-lead) and restores goldens on success.

### Step 3 — Triage & report
- **If clean:** Review open ledger items (see below) and propose next concrete work.
- **If drift:** Do **NOT** re-pin goldens to silence it. Investigate per AGENTS.md. Numeric drift from ill-conditioned QPs (SLSQP) is environment-sensitive, not a reason to overwrite baselines.

---

## Open Items (from `ledger/RESEARCH_LEDGER.md`)

1. **E049 residual — the tangency QP is still ill-conditioned.** Replace the SLSQP QP solves with a well-conditioned, deterministic solver (for N <= 5 an exact active-set enumeration of all KKT points is feasible and was used here as the reference oracle), then re-pin the affected artifacts deliberately.
2. **E049 secondary defect (deliberately not fixed):** `y0 = w_feas / max(mu_s'w_feas, 1e-12)` (`src/portfolio_opt.py:253`) masks a *negative* denominator at the 2019-10-16 rebalance. Fixing the start point would change the published numbers, so it is left for the same deliberate re-pin decision.
3. **Known reporting-only drift (do not re-pin):** E030 (near-zero quantities, input now pinned), E041 (~133 numeric diffs, 3 structural differences resolved). Both decisions and gate flags are unchanged.

---

## Guardrails (Do Not Violate)

- **Goldens are authoritative:** Never let verification overwrite committed `experiments/*.json`. The suite backs up and restores them. A half-finished run must be recovered.
- **Pre-registration first:** Any new experiment must have a pre-registered JSON block, gates, falsification expectations, and sensitivity grid before execution. Goalposts cannot be moved post-hoc.
- **MHT:** Sensitivity grids are "reported, not gated". Promotion requires a dedicated pre-registered confirmatory run with full placebo.
- **Offline discipline:** Prefer pinned data/vintages. The suite runs with `QUANT_RESEARCH_OFFLINE=1`. Unpinned inputs are not allowed.
- **Optimizer rule:** Solver exit status is not a gating criterion. Validate on problem constraints (enforced by `tests/test_portfolio_opt.py`).
- **CI:** Do not create `.github/workflows/`. Use the template in `.github/workflow-templates/` if needed.
- **Commits:** Only commit when explicitly requested. Never commit verification output or corrupted goldens.

---

## Quick References

- **Full commands:** `AGENTS.md` (Quick Start, Reproducibility, Baseline Integrity)
- **Ledger:** `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- **Extended verification:** `SEED=42 python3 run_all_verification.py --extended` (~21 min)
- **Full verification:** `SEED=42 python3 run_all_verification.py --full` (~15 min)
- **Convention check only:** `SEED=42 python3 verify_convention_robustness.py`

---

## Handoff Metadata

- **Created:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
- **Created by:** Current agentic session
- **Purpose:** Durable handoff with a clear, timestamped initial task for the next session

(End of file)
