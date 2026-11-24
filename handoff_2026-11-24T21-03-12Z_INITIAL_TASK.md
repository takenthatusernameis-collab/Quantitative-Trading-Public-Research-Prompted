# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-24T21:03:12Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` == origin/main (0 ahead, 0 behind), HEAD `dece13ef` ("chore(kilo): checkpoint agent session")
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified this session)

- `git status --porcelain`: clean (no changes). Working tree clean.
- `git rev-list --left-right --count origin/main...HEAD`: `0	0` — HEAD in sync with origin/main.
- `.verify_snapshot/ACTIVE.json`: absent — no interrupted verification run pending.
- Research phase complete (E001–E043); surviving strategies in `ledger/RESEARCH_LEDGER.md`; canonical goldens in `experiments/*.json`.
- Dependencies: not provisioned this session.
- HEAD advanced `0ce72a57` -> `dece13ef` ("chore(kilo): checkpoint agent session") since the prior handoff (`handoff_2026-11-24T21-02-41Z_INITIAL_TASK.md`).

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent experiments, run verification unprompted, move pre-registered gates, or touch golden/baseline/canonical artifacts without explicit direction.

If autonomous action is required, in order:

1. Verify and stop: confirm HEAD/cleanliness; if clean, report state and stop.
2. Reproduce (real work): `pip install -r requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended`. Report per-driver drift; do not re-pin.
3. Revisit E041/E042 QP drift only if step 2 shows a new structural difference.
4. Cleanup: propose (do not execute) `.gitignore` + `git rm --cached` plan for handoff accumulation; let user decide.
5. Pre-registered research only if explicitly requested (pre_registered block, falsification, sensitivity grid before execution).

## Guardrails

- Always use SEED=42.
- Never commit driver verification output over canonical goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent.
- Never commit secrets/keys.
- Do not manufacture another handoff refresh to look busy.

## Key references

- `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `experiments/*.json`, `scripts/check.sh`, `run_all_verification.py`

## Handoff provenance

- Durable artifact (this session): `handoff_2026-11-24T21-03-12Z_INITIAL_TASK.md` (repo root).
- This session refreshed the durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts modified. No commit made by this session (HEAD `dece13ef` predates this session).
- Symlink set repointed to this file.
(End of file)