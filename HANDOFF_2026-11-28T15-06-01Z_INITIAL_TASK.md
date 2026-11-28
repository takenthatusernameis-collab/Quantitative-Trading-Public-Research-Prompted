# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-28T15:06:01Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` (aligned with `origin/main`; HEAD `ec79d2a8`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Authoritative state snapshot

Read `.handoff.md` (created `2026-11-28T15:04:52Z`) for the verified state. It reports:

- Research phase complete (E001–E043+); dispositions in `ledger/RESEARCH_LEDGER.md`.
- `.verify_snapshot/` absent; no interrupted verification pending.
- Golden baseline possibly BROKEN at HEAD: `check_golden_baseline.py` expected to FAIL on 5 `experiments/*.json` artifacts (pure floating-point drift); recover from commit `c5038332` — do NOT re-pin.
- Data coverage PASS (35 pinned inputs).
- `numpy`/`pandas` NOT importable in this environment — run `pip install -r requirements.txt` first.
- Working tree clean of tracked source except ignored `src/__pycache__/`.

## Initial task for the next session (CLEAR, in order)

Default: await explicit user instructions. Do not invent experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

1. `git status --short --branch` — confirm HEAD/remote alignment; note uncommitted files (ignored `src/__pycache__/` is fine).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` first.
3. Install deps: `python3 -m pip install -r requirements.txt`; confirm `import numpy, pandas`.
4. Reproduce/verify baseline: `SEED=42 python3 scripts/check_golden_baseline.py` and `SEED=42 python3 scripts/check_goldens_clean.py`.
5. If the 5-file golden drift is present, recover surgically:
   ```bash
   git checkout c5038332 -- \
     experiments/cointegration_large_liquid.json \
     experiments/dollar_neutral_lowbeta_large_liquid.json \
     experiments/e037_portfolio.json \
     experiments/e042_lead_config_confirmatory.json \
     experiments/pairs_large_liquid.json
   ```
   then re-verify with `check_golden_baseline.py` → expect all 107 match.
6. `SEED=42 python3 scripts/check_data_coverage.py`.
7. Fast sanity: `SEED=42 bash scripts/check.sh`.
8. Commit the recovery ONLY if explicitly asked; never commit verification output over goldens; never re-pin baselines to silence drift.

## Guardrails

- Always use `SEED=42` for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit instruction + ledger justification.
- Do not reopen closed E049/E050 (optimizer determinism) or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer action required).
- Never log or commit secrets/keys.

## Key references

- `.handoff.md` — authoritative session state snapshot
- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json` (107), `ledger/data_baseline.json` (35) — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`

## Handoff provenance

- Durable artifact (this session): `HANDOFF_2026-11-28T15-06-01Z_INITIAL_TASK.md` (repo root).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified.
