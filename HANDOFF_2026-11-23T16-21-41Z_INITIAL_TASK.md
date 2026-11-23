# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-23T16:21:41Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `1e618988 chore(kilo): checkpoint agent session` (aligned with `origin/main`: `0  0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (at handoff, 2026-11-23T16:21:41Z)

- **Working tree:** clean (`git status --porcelain` empty).
- **HEAD alignment:** `git rev-list --left-right --count origin/main...HEAD` = `0  0`.
- **Research phase:** complete (E001–E043). Dispositions in `ledger/RESEARCH_LEDGER.md`. No actionable open research items.
- **Verification snapshot / reports:** absent; no interrupted verification pending.
- **Canonical artifacts untouched:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` inputs.
- **Note:** this file was created at explicit user request ~36s after the prior handoff (`HANDOFF_2026-11-23T16-21-05Z_INITIAL_TASK.md`). Per that prior file's own warning, do **not** manufacture handoff refreshes as a substitute for real work.

## Initial task for the next session

**Default: await explicit user instructions.** Do not invent new experiments, run the verification suite unprompted, change pre-registered gates/outcomes, or modify golden/baseline/canonical artifacts without explicit direction. If you have no explicit instruction, verifying state and stopping is a complete outcome.

If you must act autonomously, work in order:

1. Verify and stop: `git status --porcelain` and `git rev-list --left-right --count origin/main...HEAD`. Report clean/aligned and stop.
2. Reproduce (real work): `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift precisely. Do **not** re-pin artifacts to make tolerance violations disappear.
3. Guards if you touch baselines: re-run `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`; all must stay green.
4. Pre-registered research only if explicitly requested — `pre_registered` block + falsification expectations + sensitivity grid stated **before** execution.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit intentional instruction + ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer action required).
- Never commit/log secrets or keys.

## Key commands

```bash
SEED=42 bash scripts/check.sh              # fast guards (~seconds, offline)
SEED=42 python3 run_all_verification.py    # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended  # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after interrupted run
```

## Key references

- `AGENTS.md` — commands, reproducibility rules, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions
- `scripts/check.sh`, `run_all_verification.py`, `scripts/check_*.py`

## Handoff provenance

- **Durable artifact (this session):** `HANDOFF_2026-11-23T16-21-41Z_INITIAL_TASK.md` (repo root). Root-level generic `CURRENT/LATEST/NEXT/*` symlinks repointed to it.
- **Supersedes operationally:** prior handoff artifacts (retained for history; not modified).
- This session created only this durable handoff (and repointed root symlinks). No code, experiments, ledgers, baselines, or canonical artifacts modified. No commit made — left uncommitted pending explicit direction.
