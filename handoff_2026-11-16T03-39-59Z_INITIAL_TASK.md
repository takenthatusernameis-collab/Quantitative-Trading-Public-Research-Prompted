# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T03:39:59Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `06b68742` (`chore(kilo): checkpoint agent session`) on `main`
**Remote:** in sync with `origin/main` (0 0 ahead/behind).

## Project context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase **complete (E001–E043)**; surviving
validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. All experiments
are pre-registered — never move goalposts post-hoc. Close-to-close is the v1.2.3
primary convention; overnight decomposition is reported alongside.

## Current state (as of this handoff)

- **HEAD moved:** the previous handoff cited `13c6bf0e`; current HEAD is `06b68742`,
  another `chore(kilo): checkpoint agent session` commit. No research/source/data/
  experiment changes accompanied it.
- **Working tree:** no research/source/data/experiment diffs. Only pre-existing
  modified tracked `__pycache__/*.pyc` files are present (under `scripts/__pycache__/`,
  `src/__pycache__/`, `tests/__pycache__/`) — do **not** commit them.
- **No interrupted verification:** `.verify_snapshot/` and `.verify_reports/` are absent;
  canonical `experiments/*.json` goldens are intact and match HEAD plus the pinned
  fingerprints in `ledger/golden_baseline.json`.
- **Baseline integrity guards:** re-confirmed at handoff time with
  `SEED=42 bash scripts/check.sh` → exit 0 / `=== All checks passed ===`.
- **Guard output note:** the expected `FAIL` lines inside `check.sh` output are
  negative-case unit-test assertions (malformed JSON fixtures, stale snapshot,
  missing/mutated `data/panel.parquet` fixtures, unreadable manifest). The final
  line is authoritative: `=== All checks passed ===`.

## Initial task for the next agent (do first)

1. **Confirm baseline:** `SEED=42 bash scripts/check.sh` (or `make check`).
   Expect exit 0 / `=== All checks passed ===`.
2. **If a real baseline issue appears:**
   - Dirty goldens / stale `.verify_snapshot/`: `SEED=42 python3 run_all_verification.py --restore-only`
     (or restore pinned artifacts per `ledger/golden_baseline.json`). Never commit captured verification output.
   - Golden fingerprint mismatch: resolve deliberately against `ledger/golden_baseline.json`;
     do not re-pin as a side effect of verification.
   - Re-run `SEED=42 bash scripts/check.sh` after recovery.
3. **Then await explicit user direction.** Do not run long verification, invent experiments,
   or change gates/outcomes unprompted. Do not modify or re-pin `experiments/*.json`,
   `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`,
   or `data/` without explicit request and justified diff. Never leave a verification run
   half-finished.

## Quick reference

```bash
SEED=42 bash scripts/check.sh                          # fast convention + guard checks
SEED=42 python3 run_all_verification.py                # quick verification (~8 min)
SEED=42 python3 run_all_verification.py --extended     # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + 96-config grid
SEED=42 python3 verify_convention_robustness.py        # convention robustness only
SEED=42 python3 run_all_verification.py --restore-only # recover after interrupted run
```

## Open items (do not resolve silently)

- **E041 drift:** 133 numeric diffs (1-ulp QP sensitivity) remain post optimizer fix;
  decision REJECTED 3/5 unchanged. **Do not re-pin.** (ledger E049)
- **E042 lead:** PARTIAL (4/5 gates; G2 constrained placebo z 2.11 < 3.0 fails).
  The min-var confirmatory passes convention robustness; tangency-grid configs still drift.
  Do not re-pin drift away. (ledger E049)
- **CI gate:** template `.github/workflow-templates/verification-gate.yml`; a maintainer
  must create the real workflow via the GitHub UI (automated agents cannot).
- **Promotion:** any sensitivity-grid-clearing config needs a dedicated pre-registered
  confirmatory run with full placebo before promotion.

## Handoff artifact

- Primary (this file): `handoff_2026-11-16T03-39-59Z_INITIAL_TASK.md`
- Durable copy (identical): `INITIAL_TASK.md`
- Prior handoff: `handoff_2026-11-16T03-38-34Z_INITIAL_TASK.md`

---

*Generated 2026-11-16T03:39:59Z for durable handoff to the next agentic work session.*
