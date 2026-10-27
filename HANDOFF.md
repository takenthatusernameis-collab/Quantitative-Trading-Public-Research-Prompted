# HANDOFF - Next Agentic Work Session

**Timestamp (UTC):** 2026-10-27T23:39:57Z
**From:** Kilo (kilo-auto/free)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**HEAD:** fb273a5 (chore(kilo): checkpoint agent session)
**Branch:** main, up to date with origin/main

## Current State

- **Research phase complete (E001–E049).** Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Market-neutral portfolio line CLOSED (E041/E042/E042b):** E042 (min_variance β≤0.05 confirmatory) was PARTIAL 4/5 (G1/G3/G4/G5 pass; G2 β-constrained placebo z=2.11 < 3.0 failed). E042b (max_sharpe β≤0.1) also rejected (4/5). No blend of the 5 validated components is simultaneously market-neutral and placebo-significant on the free-public-data surface. Component strategies remain the surviving edges.
- **Verification hardening complete:** Golden baseline guards (`scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`), data coverage enforcement (`scripts/check_data_coverage.py` + `ledger/data_baseline.json`, 35 pinned inputs), optimizer determinism rules (validate solver answer against problem constraints, not exit status — pinned by `tests/test_portfolio_opt.py`), artifact-vs-code reconciliation policy, and extended drift reporting (`.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`, gitignored).
- **Reproducibility:** E029 fundamentals pinned (`data/fundamentals/` + `data/fundamentals_vintages.json`), E030 16-ETF panel pinned — both now offline-reproducible. E041 still shows ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP); do **not** re-pin to silence (ledger E049).
- **Working tree:** clean of tracked changes (only `__pycache__/*.pyc`, gitignored). No live verification snapshot (`.verify_snapshot/` absent, no `ACTIVE.json`). No run in progress; nothing to recover.

## Initial Task (do this first)

1. **Verify repo health (golden integrity).**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Must pass: goldens clean vs HEAD, golden baseline fingerprint match, py_compile, `tests/test_portfolio_opt.py`, convention robustness, JSON/artifact schema guards, template validation.
2. **Confirm clean baseline state.**
   ```bash
   git diff --name-only
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_data_coverage.py
   ```
   Expected: only `__pycache__/*.pyc` diffs (or none). Both checks must pass.
3. **Decide next action.**
   - If checks pass and working tree clean of tracked changes: no verification rerun needed. Review `ledger/RESEARCH_LEDGER.md` for open items.
   - If checks fail on goldens: restore before committing (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`). Do **not** re-pin artifacts as a side effect of a verification run.

## Known Pre-existing Drift (reporting-only, decisions unchanged)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned tangency QP; optimizer determinism fixed per ledger E049). 3 structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.
- **E042 lead artifact**: `/placebo_constrained` block deliberately re-pinned (E049); `/primary` block reproduces to 5e-9. Decision unchanged (REJECTED 4/5, G2 fails).

## Open Items / Candidate Next Work (all bounded, none require new data)

1. **Triage E041 residual drift** — Investigate the remaining 133 numeric diffs: better scaling/conditioning of the tangency QP, or a deterministic solver (for N≤5 an exact active-set enumeration of all KKT points is feasible and was used as the reference oracle). Do **not** re-pin goldens until the root cause is fixed; document in ledger if changes made.
2. **Harden verification** — Review extended drift reporting (`.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`, deterministic, gitignored). Only adjust tolerances/cases if justified and pre-registered.
3. **Data coverage audit** — Run `python3 scripts/check_data_coverage.py` to confirm all 35 cached inputs match pins. If adding new data, commit the file and update pins with `--update`.
4. **Docs/ledger reconciliation** — Update `ledger/RESEARCH_LEDGER.md` / `README.md` with any findings, keeping pre-registration/falsification discipline.

## Guardrails

- **Never** let verification overwrite committed goldens. The suite backs up/restores; if interrupted, restore before committing.
- **Don't re-pin** artifacts to hide stochastic/numeric drift. Follow the reconciliation rule: assert pre-registered *outcomes* (pass/fail/decision), not fixed point estimates.
- **Data inputs:** If adding new downloaded inputs, commit the file and re-pin via `python3 scripts/check_data_coverage.py --update` (must satisfy the data coverage invariant).
- **Optimizer:** Follow the pinned rule — validate solver answer against problem constraints, not solver exit status.
- **Reproducibility:** Always use `SEED=42`. Run lint/typecheck as appropriate; never commit secrets.
- **CI workflow:** cannot be created by agents (controller restores `.github/workflows/`, token lacks `workflows` scope). Template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`.

## Quick Commands

```bash
# Fast sanity check
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Recover if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

## Notes

- Stale snapshot protection is active (`.verify_snapshot/ACTIVE.json` tracks owning PID). Suite refuses to start if another live run owns it.
- Extended drift report goes to `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored).
- No new strategy family is warranted: the novelty search (E001–E049) is complete, all free public data sources are exhausted, and the market-neutral total-portfolio line is closed.