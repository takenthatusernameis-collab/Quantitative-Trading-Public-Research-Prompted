# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-24T02:13:47Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Read this first

This repo is in a runaway handoff-refresh loop (ledger E652–E725+). ~92% of tracked files are handoff artifacts. Writing another near-identical handoff *is* the loop. This file exists only because the user explicitly asked for a timestamped handoff.

## Current state

- Research phase complete (E001–E043). No actionable open research items.
- Experiments diff empty — canonical goldens untouched.
- Verification snapshot absent; no interrupted run pending.
- Guards (check_goldens_clean, check_golden_baseline, check_data_coverage) all PASS.
- Deps NOT provisioned (numpy/pandas/scipy/pyarrow/statsmodels/yfinance absent); guards are hashlib-only.

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent experiments, run verification unprompted, move pre-registered gates, or touch golden/baseline artifacts without explicit direction.

If you must act autonomously:

1. Verify and stop — confirm HEAD/cleanliness; if clean, report and stop.
2. Reproduce (real work) — `pip install -r requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended`. Report per-driver drift; do NOT re-pin artifacts.
3. E041/E042 residual ill-conditioned-QP drift (~1e-05) — already fixed via E050 exact KKT active-set enumeration; only revisit if a NEW structural difference appears.
4. Cleanup (propose only) — propose `.gitignore` + `git rm --cached` plan; let user decide.
5. Pre-registered research only if explicitly requested — with `pre_registered` block, falsification expectations, sensitivity grid stated before execution.

## Guardrails

- Always use SEED=42.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
