# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T05:37:44Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `feaa13ffe136c55aa57c99905047ba8034730941` (`chore(kilo): checkpoint agent session`) on `main`
**Remote:** `origin/main` — in sync (0 ahead, 0 behind) at handoff time

## Project context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase is **complete (E001–E043)**; surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

- **Pre-registration:** every experiment driver has a `pre_registered` JSON block and a docstring stating gates, falsification expectations, and sensitivity grid. Goalposts are never moved post-hoc.
- **Convention:** close-to-close is the v1.2.3 primary convention; overnight decomposition is reported alongside.
- **Golden baseline policy:** `experiments/*.json` are canonical artifacts. Verification overwrites them during runs and must restore them afterward. Never leave a verification run half-finished; never commit captured verification output.

## Current state (as of this handoff)

- **HEAD:** `feaa13ff` on `main`, in sync with `origin/main`. This is one checkpoint commit (`chore(kilo): checkpoint agent session`) ahead of the prior handoff's recorded HEAD `6a574c0c`. That commit touched **only** handoff symlinks and the handoff document itself — **no research, source, data, experiment, ledger, script, or test changes.**
- **Working tree:** clean except for pre-existing modified tracked `__pycache__/*.pyc` files under `scripts/__pycache__/`, `src/__pycache__/`, and `tests/__pycache__/`. Do **not** commit these `.pyc` files.
- **Interrupted verification:** none detected — `.verify_snapshot/` and `.verify_reports/` are absent; `git stash list` is empty.
- **Canonical artifacts:** `experiments/*.json` goldens and pinned fingerprints in `ledger/golden_baseline.json` / `ledger/data_baseline.json` are the authoritative baseline; integrity is guarded by `scripts/check.sh`.
- **Ledger:** `ledger/RESEARCH_LEDGER.md` (last modified 2026-11-16T03:49Z within this session) is the living record; `ledger/golden_baseline.json` and `ledger/data_baseline.json` are the pinned baselines.

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
   - Do not run long verification suites (`run_all_verification.py`, `--extended`, `--full`) unless explicitly requested.
   - Do not invent experiments or change gates/outcomes unprompted.
   - Do not modify or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`, or `data/` without an explicit request and a justified diff.
   - Never leave any verification run half-finished.

## Quick reference

```bash
SEED=42 bash scripts/check.sh                          # fast convention + guard checks (~seconds)
SEED=42 python3 run_all_verification.py                # quick verification (~8 min)
SEED=42 python3 run_all_verification.py --extended     # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + 96-config grid (~15+ min)
SEED=42 python3 verify_convention_robustness.py        # convention robustness only
SEED=42 python3 run_all_verification.py --restore-only # recover after interrupted run
```

## Open items (do not resolve silently)

- **E041 drift (ledger E049):** ~133 numeric diffs (1-ulp sensitivity of ill-conditioned QP) remain after the optimizer determinism fix; decision **REJECTED (3/5)** unchanged. **Do not re-pin.**
- **E042 lead (ledger E049):** **PARTIAL** (e.g. 4/5 gates; constrained-placebo z below threshold in prior records). Min-var confirmatory passes convention robustness; tangency/grid configs still drift — do not re-pin drift away.
- **CI gate:** template exists at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via GitHub UI (agents cannot push workflows with this token).
- **Promotion:** any sensitivity-grid-clearing config requires a dedicated pre-registered confirmatory run with a full placebo before promotion.

## Handoff artifacts

- **Primary (this file):** `handoff_2026-11-16T05-37-44Z_INITIAL_TASK.md`
- **Mirror:** `handoff/handoff_2026-11-16T05-37-44Z_INITIAL_TASK.md`
- **Prior handoff:** `handoff_2026-11-16T05-36-15Z_INITIAL_TASK.md` (recorded HEAD `6a574c0c`)

---

*Generated 2026-11-16T05:37:44Z as a durable handoff for the next agentic work session.*