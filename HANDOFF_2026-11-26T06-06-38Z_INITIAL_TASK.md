# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-26T06:06:38Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `43aa43b83aa50a6e8c731ad3c1e88d8194059399`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (as of 2026-11-26T06:06:38Z)

- **Research phase:** complete (E001–E043). Authoritative dispositions and surviving validated strategies live in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research items.
- **Working tree:** clean except `src/__pycache__/` build artifact (untracked/modified cache; not canonical). No modified tracked research artifacts this session.
- **Verification snapshot / reports:** `.verify_snapshot/` absent, `.verify_reports/` absent. No interrupted verification pending.
- **Canonical artifacts/baselines untouched:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` and `data/fundamentals/` inputs.
- **Dependencies NOT importable this session** (`import numpy` → `ModuleNotFoundError`). Run `pip install -r requirements.txt` before any verification.

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent new experiments, run the verification suite unprompted, change pre-registered gates/outcomes, or modify golden/baseline/canonical artifacts without explicit direction.

If you must act autonomously, work in order and stop when a step is genuinely done:

1. **Verify and stop.** Confirm `git status --porcelain` and `git rev-list --left-right --count origin/main...HEAD`. If HEAD is aligned and the tracked tree is clean, report that and stop.
2. **Reproduce (real work, not a handoff refresh).** `pip install -r requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift precisely. Do **not** re-pin artifacts to make any tolerance violation disappear.
3. **Guards if you touch baselines.** Re-run `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`; all must stay green.
4. **Cleanup (propose only, do not execute).** Thousands of handoff files + mirror dirs are almost certainly unwanted. *Propose* a `.gitignore` + `git rm --cached` plan (keeping a single durable `HANDOFF_<latest>.md`) and let the user decide. Do not delete unilaterally.
5. **Pre-registered research** only if the user explicitly requests it — with a `pre_registered` block, falsification expectations, and sensitivity grid stated *before* execution.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent.
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.
- **Do not manufacture another handoff refresh to look busy.**

## Key commands

```bash
# Fast guards (seconds, offline, hashlib-only)
SEED=42 bash scripts/check.sh          # or: make check

# Reproducibility / verification
SEED=42 python3 run_all_verification.py                  # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended       # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full           # n_sim=50 + 96-config grid

# Recover goldens after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Handoff provenance

- **Durable artifact (this session):** `HANDOFF_2026-11-26T06-06-38Z_INITIAL_TASK.md` (repo root).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified. No commit was made — left uncommitted pending explicit direction.
