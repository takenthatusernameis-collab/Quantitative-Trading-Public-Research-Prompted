# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC): 2026-11-15T22:44:28Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `a82758ad` (`chore(kilo): checkpoint agent session`) on `main`
**Sync:** assume `main`; confirm with `git status --short` / `git rev-list --left-right --count origin/main...HEAD` if network is available.

## Project context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase **complete (E001–E043)**; surviving validated strategies and dispositions are recorded in `ledger/RESEARCH_LEDGER.md`. All experiments are pre-registered; never move goalposts post-hoc. Close-to-close is the v1.2.3 primary convention; overnight decomposition is reported alongside every strategy.

## Current state (this session)

- **Working tree:** clean except pre-existing `__pycache__/*.pyc` churn (build artifacts, not source). `experiments/`, `ledger/`, and `data/` are unmodified versus HEAD. No staged source/data/experiment changes.
- **No interrupted verification run:** `.verify_snapshot/` and `.verify_reports/` are absent; the canonical `experiments/*.json` goldens are intact.
- **Baseline integrity:** guards reference `AGENTS.md`; run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm `=== All checks passed ===`. This includes `check_json_artifacts.py`, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `validate_template.py`, `check_experiment_imports.py`, and `verify_convention_robustness.py`.
- **Dependencies:** unit tests may not be runnable in this sandbox (missing `numpy`/`pandas`/`pytest`); unrelated to repo content. If needed: `pip3 install --break-system-packages -r requirements.txt`.
- **Last committed handoff:** `HANDOFF_2026-11-15T22-44-00Z.md` — baseline verification-first stance still applies.

## Initial task for the next agent (do first)

1. **Confirm baseline integrity**
   - Run `SEED=42 bash scripts/check.sh` (or `make check`). Expect exit 0 and `=== All checks passed ===`.
   - If it fails only because deps are missing, install `requirements.txt` and retry — that is not a baseline failure.
2. **If checks reveal a real baseline issue**
   - Dirty goldens / stale snapshot: `SEED=42 python3 run_all_verification.py --restore-only` (or restore the pinned artifacts from `ledger/golden_baseline.json`). Never commit captured verification output.
   - Re-run `SEED=42 bash scripts/check.sh` after recovery.
3. **Then proceed only with explicit user direction.**
   - Default: await instructions. Do **not** run long verification, invent experiments, or change gates/outcomes unprompted.
   - Do **not** modify or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`, or `data/` without an explicit request and a justified diff.
   - Never leave a verification run half-finished; do not commit `__pycache__`.

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

- Primary: `handoff_2026-11-15T22-44-28Z_INITIAL_TASK.md`
- Pointers/mirrors: repoint canonical `handoff/`, `HANDOFF/`, `.handoff/`, `.kilo/` aliases to this file via `python3 scripts/repoint_handoff.py handoff_2026-11-15T22-44-28Z_INITIAL_TASK.md` if that script exists; otherwise create the mirror files manually.

---

*Generated at 2026-11-15T22:44:28Z for durable handoff to the next agentic work session.*
