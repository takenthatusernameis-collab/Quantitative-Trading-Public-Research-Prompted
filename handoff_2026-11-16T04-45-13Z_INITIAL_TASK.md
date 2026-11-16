# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T04:45:13Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `f66e003b` (`chore(kilo): checkpoint agent session`) on `main`
**Remote:** `origin/main` (in sync at handoff time)

## Project context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase is **complete (E001–E043)**; surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

- **Pre-registration discipline:** every experiment is pre-registered; never move goalposts post-hoc.
- **Conventions:** close-to-close is the v1.2.3 primary convention; overnight decomposition is reported alongside.
- **Golden baseline policy:** `experiments/*.json` are canonical artifacts. Verification overwrites them during runs and must restore them; never leave a verification run half-finished and never commit captured verification output.

## Current state (as of this handoff)

- **HEAD:** `f66e003b` on `main`, in sync with `origin/main`. No research/source/data/experiment changes were made in this session.
- **Working tree:** clean except for pre-existing modified tracked `__pycache__/*.pyc` files under `scripts/__pycache__/`, `src/__pycache__/`, and `tests/__pycache__/`. Do **not** commit these `.pyc` files.
- **Interrupted verification:** none detected — `.verify_snapshot/` and `.verify_reports/` are absent.
- **Canonical artifacts:** `experiments/*.json` goldens are intact per repository state; integrity is guarded by `scripts/check.sh` / `ledger/golden_baseline.json` / `ledger/data_baseline.json`.

## Initial task for the next agent (do first)

1. **Confirm baseline integrity (required):**
   - Run: `SEED=42 bash scripts/check.sh` (or `make check`)
   - Expected: exit 0 and final line `=== All checks passed ===`
   - Note: `FAIL` lines inside `check.sh` output may appear as negative-case unit-test assertions; the final summary line is authoritative.
2. **If a real baseline issue is detected:**
   - Dirty goldens / stale `.verify_snapshot/`: run `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `ledger/golden_baseline.json` as documented in `AGENTS.md`). Never commit captured verification output.
   - Golden fingerprint mismatch: resolve deliberately against `ledger/golden_baseline.json`; do **not** re-pin as a side effect of verification.
   - Re-run `SEED=42 bash scripts/check.sh` after recovery and ensure it passes.
3. **After baseline is confirmed, await explicit user direction.**
   - Do not run long verification suites, invent experiments, or change gates/outcomes unprompted.
   - Do not modify or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`, or `data/` without an explicit request and a justified diff.
   - Never leave any verification run half-finished.

## Quick reference

```bash
SEED=42 bash scripts/check.sh                          # fast convention + guard checks (~seconds)
SEED=42 python3 run_all_verification.py                # quick verification (~8 min)
SEED=42 python3 run_all_verification.py --extended     # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + 96-config grid (~15+ min)
SEED=42 python3 verify_convention_robustness.py        # convention robustness only
SEED=42 python3 run_all_verification.py --restore-only # recover after interrupted verification
```

## Open items (do not resolve silently)

- **E041 drift (ledger E049):** 133 numeric diffs (1-ulp QP sensitivity) remain after optimizer fix; decision **REJECTED (3/5)** unchanged. **Do not re-pin.**
- **E042 lead (ledger E049):** **PARTIAL** (e.g. 4/5 gates; constrained-placebo z below threshold in prior records). Min-var confirmatory passes convention robustness; tangency/grid configs still drift — do not re-pin drift away.
- **CI gate:** template exists at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via GitHub UI (agents cannot push workflows with this token).
- **Promotion:** any sensitivity-grid-clearing config requires a dedicated pre-registered confirmatory run with a full placebo before promotion.

## Handoff artifact

- **Primary (this file):** `handoff_2026-11-16T04-45-13Z_INITIAL_TASK.md`
- **Prior handoff:** `handoff_2026-11-16T04-43-47Z_INITIAL_TASK.md`
- **Durable pointers updated to this handoff:** `INITIAL_TASK.md`, `LATEST.md`, `LATEST`, `HANDOFF_LATEST`, `LATEST_INITIAL_TASK`, `HANDOFF_INITIAL_TASK_LATEST`, `HANDOFF_NEXT_SESSION`, `NEXT_SESSION`, `HANDOFF_NEXT`, `NEXT`, `NEXT.md`, `NEXT_SESSION.md`, `HANDOFF_CURRENT`, `CURRENT.md`

---
*Generated 2026-11-16T04:45:13Z as a durable handoff for the next agentic work session.*
