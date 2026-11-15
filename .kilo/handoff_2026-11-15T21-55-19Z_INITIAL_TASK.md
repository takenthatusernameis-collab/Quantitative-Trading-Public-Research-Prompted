# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC): 2026-11-15T21:55:19Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `1af36caa56e918ca5d618001cc3b45507aeb7998` (`chore(kilo): checkpoint agent session`) on `main`
**Sync:** `git rev-list --left-right --count origin/main...HEAD` → `0	0` (in sync with `origin/main`)
**Prior handoff superseded:** `handoff_2026-11-15T20-47-57Z_INITIAL_TASK.md` (retained for history)

## Project context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase is **complete (E001–E051)**; surviving validated strategies and every disposition are recorded in `ledger/RESEARCH_LEDGER.md`. All experiments are pre-registered — never move goalposts post-hoc. Close-to-close is the v1.2.3 primary convention; overnight decomposition is reported alongside for every strategy.

## Current state (verified this session)
- **Working tree:** clean except pre-existing modified `__pycache__/*.pyc` files under `scripts/`, `src/`, `tests/` (gitignored/build artifacts — **do not commit**). No tracked source, experiment, data, golden, or ledger content changed. No untracked files added.
- **No interrupted verification run:** `.verify_snapshot/` and `.verify_reports/` are absent; canonical `experiments/*.json` goldens are intact.
- **Baseline integrity — `SEED=42 bash scripts/check.sh` exit 0:** JSON artifacts parse, goldens match HEAD and pinned SHA-256 baseline (`ledger/golden_baseline.json`), data coverage OK (`ledger/data_baseline.json`), template/import checks OK, convention robustness passed (`ALL VERIFICATIONS PASSED`).

## Clear initial task for the next agent (do first)
1. **Confirm baseline integrity**
   - Run `SEED=42 bash scripts/check.sh` (or `make check`). Expect exit 0 and `=== All checks passed ===`.
   - If it fails only because dependencies are missing, install `pip install -r requirements.txt` and retry — that is not a baseline failure.
2. **If checks reveal a real baseline issue**
   - Dirty goldens / stale snapshot: `SEED=42 python3 run_all_verification.py --restore-only` (or restore the pinned artifacts from `ledger/golden_baseline.json`). Never commit captured verification output.
   - Re-run `SEED=42 bash scripts/check.sh` after recovery.
3. **Then proceed only with explicit user direction.**
   - Default: report status and await instructions. Do **not** run long verification, invent experiments, or change gates/outcomes unprompted.
   - Do **not** modify or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`, or `data/` without an explicit request and a justified diff.
   - Never leave a verification run half-finished; do not commit `__pycache__/`, `.verify_snapshot/`, or `.verify_reports/`.

## Quick reference
```bash
SEED=42 bash scripts/check.sh                         # fast convention + guard checks (seconds)
SEED=42 python3 run_all_verification.py               # quick verification (~8 min)
SEED=42 python3 run_all_verification.py --extended    # +18 more committed drivers (~21 min)
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 verify_convention_robustness.py       # convention robustness only (reads JSONs)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after interrupted run
```

## Open items (do not resolve silently)
- **E041 drift:** 133 numeric differences (1-ulp QP sensitivity of an ill-conditioned optimizer) remain after the optimizer fix; decision REJECTED 3/5 unchanged. **Do not re-pin to silence.** See ledger E049.
- **E042 lead:** PARTIAL (3/5 gates). Min-var confirmatory run (n_sim=50) passes convention robustness but the tangency grid drifts. See ledger E049.
- **Optimizer determinism rule** (ledger E049): `src/portfolio_opt.py` validates a solver answer on the *problem's constraints*, never on the solver exit status; pinned by `tests/test_portfolio_opt.py`.
- **Extended drift report:** `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` is gitignored / reporting-only when produced by `--extended`.
- **CI gate:** `.github/workflows/verification-gate.yml` cannot be created by automated agents here (controller cleans `.github/workflows/`; token lacks `workflows` scope). A maintainer must add it via GitHub UI from `.github/workflow-templates/verification-gate.yml`; see `VERIFICATION_GATE_TEMPLATE.md`.
- **Promotion gates:** any config clearing a sensitivity grid requires a dedicated pre-registered confirmatory run with a full placebo before promotion.

## Guardrails
- Always `SEED=42`.
- Never commit verification output; never modify `experiments/*.json` goldens except an explicit, reviewed re-pin via `python3 scripts/check_golden_baseline.py --update` (never to silence drift).
- Do not move pre-registered goalposts, gates, sensitivity grids, or validated constructions post-hoc. Negative results stay recorded honestly (REJECTED / PARTIAL).
- Re-pin data inputs only via `python3 scripts/check_data_coverage.py --update` after committing the new file.

## Handoff artifact
- Primary: `handoff_2026-11-15T21-55-19Z_INITIAL_TASK.md`
- Generic canonical pointers should be repointed to this file (e.g. via `python3 scripts/repoint_handoff.py handoff_2026-11-15T21-55-19Z_INITIAL_TASK.md`).

---
*Generated at 2026-11-15T21:55:19Z for durable handoff to the next agentic work session.*
