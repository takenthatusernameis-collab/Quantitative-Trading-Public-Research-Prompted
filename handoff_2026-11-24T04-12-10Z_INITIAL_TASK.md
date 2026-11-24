# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-24T04:12:10Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## CLEAR INITIAL TASK for the next session

**Default: await explicit user instructions.** Do not invent experiments, do not
run the verification suite unprompted, do not move pre-registered gates, and do
not touch golden/baseline/canonical artifacts without explicit direction.

If you must act autonomously, work top-to-bottom and stop as soon as a step is
genuinely done:

1. **Verify and stop.** Confirm cleanliness and sync
   (`git status --porcelain`,
   `git rev-list --left-right --count origin/main...HEAD`). If clean and in
   sync, report state and stop — that is a complete, correct outcome.
2. **Reproduce (real work, not a handoff refresh).**
   `pip install -r requirements.txt`, then
   `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report
   per-driver drift precisely. **Never** re-pin an artifact to make a tolerance
   violation disappear. Quick convention check first:
   `SEED=42 bash scripts/check.sh` (or `make check`).
3. **Handoff-farm cleanup (propose only).** The repo carries hundreds of
   `handoff_*` files plus generic symlinks (`handoff_LATEST.md`, `latest.md`, etc.).
   If this is a problem, *propose* (do not execute) a `.gitignore` +
   `git rm --cached` consolidation plan and let the user decide.
4. **Pre-registered research** only if the user explicitly requests it — with a
   `pre_registered` block, falsification expectations, and a sensitivity grid
   stated *before* execution.

## Guardrails

- Always use **SEED=42** for reproducibility/verification.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
  If a run is interrupted, restore first:
  `SEED=42 python3 run_all_verification.py --restore-only`.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json`
  without an explicit, intentional re-baseline instruction and a ledger entry
  justifying it.
- Do not reopen closed items E049/E050 or the E041/E042 drift.
- Do not create `.github/workflows/` CI gates as an automated agent.
- Never commit secrets/keys; never log secrets.
- Do not manufacture handoff refreshes to look busy — one durable file per session is enough.

## Handoff provenance

- **Durable artifact (this session):**
  `handoff_2026-11-24T04-12-10Z_INITIAL_TASK.md` (repo root, this file).
- Supersedes `handoff_2026-11-24T04-11-45Z_INITIAL_TASK.md` and all older
  `handoff_*` / `HANDOFF_*` files.
- No code, experiments, ledgers, baselines, or canonical artifacts were modified.

(End of file)
