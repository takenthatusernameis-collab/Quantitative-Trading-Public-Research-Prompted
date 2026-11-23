# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-23T14:31:12Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `65d5907511d7947b10ab45b08d7e46d2a4603adc` (2026-11-23 14:31:12 +0000)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified this session)

- **HEAD ↔ origin/main in sync**: `git rev-list --left-right --count origin/main...HEAD` → `0 0` (no ahead/behind).
- **Working tree clean** (no untracked/modified source artifacts).
- **No interrupted verification snapshot pending** (`.verify_snapshot/ACTIVE.json` absent).
- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Canonical golden artifacts in `experiments/*.json`; pinned fingerprints in `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- Dependencies NOT provisioned (no `requirements.txt` install run this session).

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent experiments, run verification unprompted, move pre-registered gates, or touch golden/baseline/canonical artifacts without explicit direction.

If you must act autonomously, work in order and stop when a step is done:

1. **Verify and stop.** Confirm HEAD/cleanliness (`git status --porcelain`, `git rev-list --left-right --count origin/main...HEAD`). If clean, report state and stop — that is a complete, correct outcome.
2. **Reproduce (real work, not a handoff refresh).** `pip install -r requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift precisely; **do not** re-pin artifacts to make a tolerance violation disappear.
3. **E041/E042 residual ill-conditioned-QP drift (~1e-05):** already root-caused and fixed via the E050 exact KKT active-set enumeration (ledger E049/E050, commit `72dc947`). Only revisit if step 2 shows a *new* structural difference; never "fix" it by re-pinning.
4. **Cleanup (propose only).** If the ~8,000 handoff files are a problem, *propose* (do not execute) a `.gitignore` + `git rm --cached` cleanup plan and let the user decide.
5. **Pre-registered research** only if the user explicitly requests it — with a `pre_registered` block, falsification expectations, and sensitivity grid stated *before* execution.

## Guardrails

- Always use **SEED=42** for reproducibility/verification.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Never commit secrets/keys; never log secrets.
- Do not manufacture another handoff refresh to look busy.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-23T14-31-12Z_INITIAL_TASK.md` (repo root).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified. No commit was made (left uncommitted pending explicit direction).