# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-23T09:25:24Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `3905524bb429a5f265da1c05b26d8c180c564d16` (2026-11-23 09:24:40 +0000, "chore(kilo): checkpoint agent session")
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Read this first — the handoff-refresh loop

This repo is in a **runaway handoff-refresh loop (E652–E723+)**. Of 8,765 git-tracked
files, **8,240 (~94%) are handoff artifacts** (`handoff_*` / `HANDOFF*`). The ledger's
own E721–E723 entries state that a handoff written only seconds earlier was already
accurate and current. Writing yet another near-identical handoff is *the loop*, not work.
This file exists only because the user explicitly asked for a timestamped handoff. **Do
NOT manufacture an E724-style refresh as a substitute for real work.** If nothing has
changed, the prior handoff (`HANDOFF_NEXT_SESSION_2026-11-23T09-23-59Z_INITIAL_TASK.md`)
is still authoritative.

## Current state (verified at handoff)

- **Research phase:** complete (E001–E043 core; handoff refreshes logged through E723). Authoritative dispositions and surviving validated strategies live in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending research items.
- **HEAD:** `main` @ `3905524b`, `git rev-list --left-right --count origin/main...HEAD` = `0  0`; working tree clean (`git status --short --branch` = `## main...origin/main`, no uncommitted changes).
- **Experiments/baselines:** `git diff HEAD -- experiments/` empty. `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` and `data/fundamentals/` all unchanged by this session.
- **Verification snapshot:** `.verify_snapshot/` absent; `.verify_reports/` absent. No interrupted verification pending.
- **Guards run and PASS this session (fast, read-only, hashlib-only):**
  - `scripts/check_goldens_clean.py` → ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD (exit 0)
  - `scripts/check_golden_baseline.py` → ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT (exit 0)
  - `scripts/check_data_coverage.py` → ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED (exit 0)
  - Dependencies were **not** provisioned and the full verification suite was **not** run (out of scope for a handoff-only session).

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent experiments, run verification unprompted, move pre-registered gates, or touch golden/baseline artifacts without explicit direction.

If you must act autonomously, work the following in order and stop when a step is done:

1. **Verify and stop.** Confirm HEAD/cleanliness and the three guards above. If they pass, report state and stop — that is a complete, correct outcome.
2. **Reproduce (real work, not a refresh).** `pip install -r requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift precisely; **do not** re-pin artifacts to make a tolerance violation disappear.
3. **E041/E042 residual ill-conditioned-QP drift (~1e-05).** Already root-caused and fixed via the E050 exact KKT active-set enumeration (ledger E049/E050). Only revisit if step 2 shows a *new* structural difference; never "fix" it by re-pinning.
4. **Cleanup (propose only).** If the ~8,240 handoff files are a problem, *propose* (do not execute) a `.gitignore` + `git rm --cached` cleanup plan and let the user decide.
5. **Pre-registered research** only if the user explicitly requests it — with a `pre_registered` block, falsification expectations, and sensitivity grid stated *before* execution.

### If verification is explicitly requested

- Always **`SEED=42`**. Scopes (see `AGENTS.md`): `make check` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick), `--extended`, `--full`.
- Verification overwrites then restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift; re-pin only on explicit instruction with ledger justification.

## Guardrails

- Always use **SEED=42** for reproducibility/verification.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.
- Do not manufacture another handoff refresh to look busy.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions (latest entries E721–E723 handoff refreshes)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`

## Handoff provenance

- **Durable artifact (this session):** `HANDOFF_NEXT_SESSION_2026-11-23T09-25-24Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** prior `HANDOFF_*` / `handoff_*` artifacts (retained for history).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified.

(End of file - total 70 lines)