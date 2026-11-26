# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-26T06:07:39Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `3b7e327c2c6062e0ae643885072b7d7befeb1066`
**Upstream:** aligned with `origin/main` (`git rev-list --left-right --count origin/main...HEAD` = `0	0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (as of 2026-11-26T06:07:39Z)

- **Research phase:** complete (E001–E043). Authoritative dispositions and surviving validated strategies live in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research items.
- **Working tree:** only stray `src/__pycache__/cache_keys.cpython-312.pyc` (untracked/modified noise); no tracked-file changes this session.
- **Verification snapshot / reports:** `.verify_snapshot/` absent, `.verify_reports/` absent. No interrupted verification pending.
- **Canonical artifacts/baselines untouched:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` and `data/fundamentals/` inputs.
- **Dependencies NOT importable this session** (`import numpy` → `ModuleNotFoundError`). Run `pip install -r requirements.txt` before any verification.

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent new experiments, run the verification suite unprompted, change pre-registered gates/outcomes, or modify golden/baseline/canonical artifacts without explicit direction.

If you must act autonomously, work in order and stop when a step is genuinely done:

1. **Verify and stop.** Confirm `git status --porcelain` and `git rev-list --left-right --count origin/main...HEAD`. If HEAD is aligned and the tracked tree is clean, report that and stop.
2. **Reproduce (real work, not a handoff refresh).** `pip install -r requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift precisely. Do **not** re-pin artifacts to make any tolerance violation disappear.
3. **Guards if you touch baselines.** Re-run `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`; all must stay green.
4. **Cleanup (propose only, do not execute).** Thousands of handoff files + mirror dirs are almost certainly unwanted. *Propose* a `.gitignore` + `git rm --cached` plan and let the user decide. Do not delete unilaterally.
5. **Pre-registered research** only if the user explicitly requests it.

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
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
```

## Handoff provenance

- **Durable artifact (this session):** `HANDOFF_2026-11-26T06-07-39Z_INITIAL_TASK.md` (repo root).
- **No new aliases and no mirror dirs created.**
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified. No commit was made — left uncommitted pending explicit direction.

(End of file)
