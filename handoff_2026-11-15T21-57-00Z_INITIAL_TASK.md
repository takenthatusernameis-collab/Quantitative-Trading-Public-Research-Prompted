# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T21:57:00Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `61118c0c` ("chore(kilo): checkpoint agent session")
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree (non-handoff):** only `__pycache__/*.pyc` churn under `scripts/`, `src/`, `tests/` (gitignored build artifacts — **do not commit**). No source, `experiments/*.json`, ledger-baseline, or pinned-data changes.
- **Sync:** `git rev-list --left-right --count origin/main...HEAD` → `0 0` (in sync with `origin/main`).
- **Interrupted verification:** `.verify_snapshot/` and `.verify_reports/` absent.
- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies: `ledger/RESEARCH_LEDGER.md`. No open/pending/blocked research items.
- **Closed — do not reopen:** E049/E050 (optimizer determinism / exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Baseline integrity (verified this session, per-step isolation, no verification run)

All repo-level guard steps **exit 0**:

- `SEED=42 bash scripts/check.sh` → `=== All checks passed ===` (JSON artifacts, goldens clean, golden baseline SHA-256, data coverage, template, experiment imports, convention robustness)
- `python3 -c "import numpy, pandas, scipy"` → deps present in this sandbox (unit tests may still need `pytest`)

## Initial task for next session (CLEAR)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote; note `__pycache__`/handoff noise is expected.
2. Confirm baseline: `SEED=42 bash scripts/check.sh` (expect `=== All checks passed ===`).
3. If a real baseline issue appears: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`), then re-run `scripts/check.sh`. Never commit captured verification output.

## Quick reference

```bash
SEED=42 bash scripts/check.sh                       # fast convention + guard checks (seconds)
SEED=42 python3 run_all_verification.py             # quick verification (~8 min)
SEED=42 python3 run_all_verification.py --extended  # +18 more committed drivers (~21 min)
SEED=42 python3 run_all_verification.py --full      # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 verify_convention_robustness.py     # convention robustness only (reads JSONs)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after an interrupted run
```

## Open items (do not resolve silently)

- **E041 drift:** 133 numeric differences (1-ulp QP sensitivity) remain after the optimizer fix; decision REJECTED 3/5 unchanged. **Do not re-pin to silence.** See ledger E049.
- **E042 lead:** PARTIAL (3/5 gates). Min-var confirmatory run (n_sim=50) passes convention robustness but the tangency grid drifts. See ledger E049.
- **CI gate:** template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via the GitHub UI (automated agents cannot push workflows).
- **Promotion gates:** any config clearing a sensitivity grid requires a dedicated pre-registered confirmatory run with full placebo before promotion.

## Handoff artifact

- Primary: `handoff_2026-11-15T21-57-00Z_INITIAL_TASK.md`
- Mirrored identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- Generic canonical pointers repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-15T21-57-00Z_INITIAL_TASK.md`.

---
*Generated at 2026-11-15T21:57:00Z for durable handoff to the next agentic work session.*