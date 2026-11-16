# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T01-37-58Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `751b1498d90e4cd042927cafb7856e312d758463` (`chore(kilo): checkpoint agent session`) on `main`
**Remote sync:** in sync with `origin/main` at handoff time.

## Project context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase **complete (E001–E051)**; surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

- All experiments are pre-registered; never move goalposts post-hoc.
- v1.2.3 convention: close-to-close primary, overnight decomposition reported alongside.
- `experiments/*.json` are canonical golden artifacts; never capture/commit verification output as new baseline.

## Current state (verified from repo at handoff)

- **Working tree:** clean except pre-existing modified tracked `__pycache__/*.pyc` files (e.g. `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/`). **Do not commit them.** No research/source/data/experiment changes staged or made in this session.
- **No interrupted verification markers observed:** `.verify_snapshot/` and `.verify_reports/` absent at repo root.
- **Latest durable handoff:** `handoff_2026-11-16T01-36-51Z_INITIAL_TASK.md` (HEAD same as current). That handoff records `SEED=42 bash scripts/check.sh` → exit 0 / `=== All checks passed ===` after installing deps in that sandbox. Treat as last known-good baseline snapshot; re-confirm in your environment if anything changes.
- **Environment caveat:** a fresh sandbox may lack `numpy`/`pandas`/`scipy`/`statsmodels`/`yfinance`; `scripts/check.sh` can fail with `ModuleNotFoundError` until dependencies are installed. This is environmental, not a repo-content failure.

## Initial task for the next agent (do first)

1. **Install dependencies if missing (fresh sandbox):**
   - `python3 -m pip install --break-system-packages -r requirements.txt`
2. **Confirm baseline integrity (fast, offline):**
   - `SEED=42 bash scripts/check.sh` (or `make check`)
   - Expect: exit 0 and `=== All checks passed ===`.
3. **If a baseline/integrity issue is reported, recover deliberately:**
   - Dirty goldens / stale `.verify_snapshot/` / interrupted run: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `ledger/golden_baseline.json`). Never leave a verification run half-finished; never commit captured verification output.
   - Golden fingerprint mismatch: resolve against `ledger/golden_baseline.json` / `ledger/data_baseline.json` intentionally. **Do not re-pin** as a side effect of running verification.
   - Re-run `SEED=42 bash scripts/check.sh` after recovery.
4. **Then stop and await explicit user direction.**
   - Do not run long verification (`make verify-quick/extended/full`), invent experiments, modify gates/outcomes, or change research artifacts unprompted.
   - Do not modify or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`, or `data/` without explicit request and a justified diff.

## Quick reference

```bash
python3 -m pip install --break-system-packages -r requirements.txt  # deps (fresh sandbox)
SEED=42 bash scripts/check.sh                          # fast convention + guard checks
SEED=42 python3 run_all_verification.py                # quick verification (~8 min)
SEED=42 python3 run_all_verification.py --extended     # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + 96-config grid
SEED=42 python3 verify_convention_robustness.py        # convention robustness only
SEED=42 python3 run_all_verification.py --restore-only # recover after interrupted run
```

## Open items (do not resolve silently)

- **E041 drift:** 133 numeric diffs (1-ulp QP sensitivity) remain post optimizer fix; decision REJECTED 3/5 unchanged. **Do not re-pin.** (ledger E049)
- **E042 lead:** PARTIAL (3/5 gates); min-var confirmatory (n_sim=50) passes convention robustness but tangency grid drifts. (ledger E049)
- **CI gate:** template `.github/workflow-templates/verification-gate.yml` only; a maintainer must create the real workflow via the GitHub UI (automated agents cannot).
- **Promotion discipline:** any sensitivity-grid-clearing config requires a dedicated pre-registered confirmatory run with full placebo before promotion.

## Handoff artifact

- **Primary:** `handoff_2026-11-16T01-37-58Z_INITIAL_TASK.md`
- After creation, repoint generic canonical handoff pointers:
  - `python3 scripts/repoint_handoff.py handoff_2026-11-16T01-37-58Z_INITIAL_TASK.md`
- Mirror identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` (and keep existing generic symlinks/pointers consistent as done by repo conventions).

---
*Generated 2026-11-16T01-37-58Z as a clear durable initial task handoff for the next agentic work session. No research artifacts modified.*