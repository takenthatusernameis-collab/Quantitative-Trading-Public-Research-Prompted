# Initial Task (for next agentic work session)

**Timestamp (UTC):** 2026-11-18T05:40:01Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## 1) First action (do this immediately)

Run the fast integrity gate and confirm a clean baseline before making changes:

```bash
SEED=42 make check
```

If `make check` fails due to golden/data coverage/baseline drift, stop and resolve that first (do not paper over by re-running verification blindly). See `AGENTS.md` section "Baseline Integrity".

## 2) Current project state (context)

- Research phase is complete: E001–E043 documented; surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` (goldens). Verification may overwrite them during runs and restores afterwards; never leave a verification run half-finished.
- Reproducibility: use `SEED=42`. Data cache vintages pinned (`data/vintages.json`, `data/fundamentals_vintages.json`); offline coverage enforced via `ledger/data_baseline.json` and `scripts/check_data_coverage.py`.
- Optimizer note: `src/portfolio_opt.py` validates on constraints (SLSQP status 8 can be acceptable at a constrained optimum); see `AGENTS.md`.

## 3) Common verification entry points

```bash
SEED=42 make verify-quick        # ~8 min
SEED=42 make verify-extended     # ~21 min
SEED=42 make verify-full         # ~15 min
```

If interrupted, recover goldens:

```bash
SEED=42 python3 run_all_verification.py --restore-only
# or: git checkout -- experiments/
```

## 4) Open items / cautions

- Do not re-pin goldens casually. `ledger/golden_baseline.json` pins SHA-256 set; re-pinning requires intent and should be reflected in ledger/diffs.
- Known numeric drift notes (do not re-pin to silence): E041 retains ~133 numeric differences from 1-ulp QP sensitivity in extended comparisons; E042 grid artifacts can drift similarly (see `AGENTS.md`).
- CI workflow template exists at `.github/workflow-templates/verification-gate.yml` (maintainer must create real workflow via GitHub UI).

## 5) Suggested next steps (pick one)

- A. Validate repo health: run `make check`, then optionally `SEED=42 make verify-quick`; report pass/fail and any drift.
- B. Investigate/continue a specific experiment: name the experiment file and exact goal; confirm pre-registered gates before changing code.
- C. Documentation/ledger work only (no experiment reruns) unless explicitly requested.

If unclear, ask one precise clarifying question or run `make check` and summarize results.

---
*Durable handoff created 2026-11-18T05:40:01Z. Update `.handoff/latest`/symlink set when handing off again.*
