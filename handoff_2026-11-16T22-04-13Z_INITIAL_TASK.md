# Agentic Work Session Handoff — INITIAL TASK

**Timestamp:** 2026-11-16T22:04:13Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial Task Message

You are starting a new agentic work session on an independent, reproducible
quantitative-strategy research repository (2014–2026 US equities, futures, and
macro data). All experiments E001–E043 are pre-registered with falsification
expectations and promotion gates. The research phase is complete; surviving
validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

Your job on entry is to orient, verify the environment, and then proceed with the
verification level or individual experiment work requested by the operator.
Do NOT commit anything, do NOT modify `experiments/*.json` goldens, and do NOT
leave a verification run half-finished.

### Orientation checklist (run these first)

1. Read this handoff, then `AGENTS.md` and `ledger/RESEARCH_LEDGER.md`.
2. Confirm no verification run is active and the golden artifacts are clean:
   ```bash
   ls -la .verify_snapshot 2>/dev/null || echo 'no snapshot'
   git status --short experiments/
   SEED=42 python3 scripts/check_goldens_clean.py
   SEED=42 python3 scripts/check_golden_baseline.py
   ```
3. Run the fast, offline convention check (~seconds):
   ```bash
   SEED=42 bash scripts/check.sh      # or: make check
   ```

### Key Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
make verify-full

# Recover the golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

### Non-Negotiable Constraints

- **Seed**: always `SEED=42`.
- **Golden files**: `experiments/*.json` are the canonical artifacts. The
  verification suite backs them up and restores them; never commit verification
  output. If a run is interrupted, restore with
  `SEED=42 python3 run_all_verification.py --restore-only` (or
  `git checkout <commit> -- experiments/<file>` against the pinned commit in
  `ledger/golden_baseline.json`). Re-pin a golden only deliberately, never as a
  side effect of running verification.
- **Data**: cached parquet in `data/` is gitignored except the pinned vintages;
  cache coverage is an enforced invariant. The suite runs with
  `QUANT_RESEARCH_OFFLINE=1` and fails hard on a missing cache entry.
- **Dependencies**: `pip install -r requirements.txt`
  (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; `cvxpy`/`cvxopt`
  optional).
- **Do not commit** unless the operator explicitly asks.

### Known Open Items

- E041/E042 tangency QP is ill-conditioned; a 1-ulp input perturbation moves
  `min_var` answers by ~1e-05, so the extended block still reports E041 as
  drifting (133 numeric diffs). Do **not** re-pin to silence this — see the open
  item in the ledger and AGENTS.md "Optimizer determinism" (ledger E049).
- `.github/workflows/verification-gate.yml` cannot be created by automated
  agents; a maintainer must create it from
  `.github/workflow-templates/verification-gate.yml`.

### Suggested First Action

Run `SEED=42 bash scripts/check.sh`. If it passes, report the result and ask the
operator which verification level (quick / extended / full) or individual
experiment they want executed next.

---
*Generated automatically for session handoff.*