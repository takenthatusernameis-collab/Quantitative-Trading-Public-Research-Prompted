# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-26T06:08:11Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `f45240d16ba6986daf01eab0066fc14af3807fb4`
**Upstream:** aligned with `origin/main` (`git rev-list --left-right --count origin/main...HEAD` = `0	0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (as of 2026-11-26T06:08:11Z)

- **Research phase:** complete (E001–E043). Authoritative dispositions in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research items.
- **Working tree:** one modified tracked file `src/__pycache__/cache_keys.cpython-312.pyc` (bytecode, incidental). No source/baseline changes.
- **Verification snapshot / reports:** `.verify_snapshot/` absent, `.verify_reports/` absent. No interrupted verification pending.
- **Canonical artifacts/baselines untouched:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` and `data/fundamentals/` inputs.
- **Dependencies NOT importable this session** (`import numpy` → `ModuleNotFoundError`). Run `pip install -r requirements.txt` before any verification.

## Repo hygiene warning (read first)

This repository has a runaway handoff-refresh problem (~94% of tracked files are handoffs). The next session must NOT manufacture a handoff refresh as a substitute for real work. If you have no explicit user instruction, verifying state and stopping is a complete, correct outcome.

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent new experiments, run the verification suite unprompted, change pre-registered gates/outcomes, or modify golden/baseline/canonical artifacts without explicit direction.

If you must act autonomously, work in order and stop when a step is genuinely done:

1. **Verify and stop.** Confirm `git status --porcelain` and `git rev-list --left-right --count origin/main...HEAD`. If HEAD is aligned and the tracked tree is clean (aside from incidental bytecode), report that and stop.
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
SEED=42 bash scripts/check.sh          # or: make check
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --restore-only
```

## Key references

- `AGENTS.md` — commands, reproducibility rules, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts

## Handoff provenance

- **Durable artifact (this session):** `HANDOFF_2026-11-26T06-08-11Z_INITIAL_TASK.md` (repo root). `CURRENT.md` and `current.md` repoint to this file so the next session resolves `current` to it.
- **No new aliases and no mirror dirs created.**
- **Supersedes operationally:** `HANDOFF_2026-11-26T05-09-35Z_INITIAL_TASK.md` (and all prior `HANDOFF_*` / `handoff_*` artifacts, retained for history; not modified).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified. No commit was made — left uncommitted pending explicit direction.
(End of file)
