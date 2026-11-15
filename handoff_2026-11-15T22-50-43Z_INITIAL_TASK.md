# Handoff — Initial Task for Next Agentic Session

**Timestamp (UTC):** 2026-11-15T22:50:43Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `aaa20afb` (`chore(kilo): checkpoint agent session`), in sync with `origin/main`
**Working tree:** clean of research/source/data/experiment changes (only pre-existing modified tracked `__pycache__/*.pyc` files present — do not commit them)
**Verification state:** no `.verify_snapshot/` or `.verify_reports/` present; canonical `experiments/*.json` goldens intact.

## Project context
Independent reproducible quantitative-strategy research on 2014–2026 US equities/futures/macro data. **Research phase complete (E001–E043)**. Surviving validated strategies: `ledger/RESEARCH_LEDGER.md`. All experiments pre-registered (gates/falsification fixed); close-to-close is v1.2.3 primary convention with overnight decomposition reported alongside.

## Initial task (do first)
1. **Confirm baseline:** `SEED=42 bash scripts/check.sh` (or `make check`). Expect exit 0 / `=== All checks passed ===`. If failure is only missing deps, `pip install -r requirements.txt` and retry — not a baseline failure.
2. **If a real baseline/guard issue appears:**
   - Dirty goldens or stale `.verify_snapshot/`: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `ledger/golden_baseline.json` / `git checkout -- experiments/` as appropriate). Never commit captured verification output.
   - Re-run `SEED=42 bash scripts/check.sh` after recovery.
3. **Await explicit user direction** before further work. Do not run long verification (`run_all_verification.py`, extended/full) or modify research artifacts unprompted.

## Guardrails
- Always use `SEED=42` for verification/runs. Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`).
- Never leave a verification run half-finished; never commit verification output. Committed golden baseline is authoritative (`ledger/golden_baseline.json`, `ledger/data_baseline.json`).
- Do not modify or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`, or `data/` without explicit request and a justified diff. Do not re-pin to silence drift.
- Known open items (do not resolve silently): **E041** has 133 residual numeric diffs (1-ulp QP sensitivity, decision REJECTED 3/5 unchanged — do not re-pin, ledger E049); **E042** PARTIAL (3/5). CI gate is template-only (`.github/workflow-templates/verification-gate.yml`).

## Quick reference
```bash
SEED=42 bash scripts/check.sh                          # fast integrity/guards (~seconds)
SEED=42 python3 run_all_verification.py                # quick verification (~8 min)
SEED=42 python3 run_all_verification.py --extended     # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + grid (~15 min)
SEED=42 python3 run_all_verification.py --restore-only # recover interrupted run
```

Key docs: `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `README.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
