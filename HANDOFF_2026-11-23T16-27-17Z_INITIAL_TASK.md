# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-23T16:27:17Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `6aa51efd chore(kilo): checkpoint agent session` (aligned with `origin/main`: `0  0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff, 2026-11-23T16:27:17Z)

- **Working tree:** clean (`git status --porcelain` empty; `git status --short --branch` shows `## main...origin/main` with no uncommitted changes).
- **HEAD alignment:** `git rev-list --left-right --count origin/main...HEAD` = `0  0`. HEAD `6aa51efd756c75a1072a713a883555d8583c412a`.
- **Research phase:** complete (E001–E043). Dispositions in `ledger/RESEARCH_LEDGER.md` (ledger tail: E726 durable-handoff-refresh entry, 2026-11-23T10:31:06Z). No actionable open research items.
- **Verification snapshot / reports:** absent (`.verify_snapshot/` and `.verify_reports/` do not exist). No interrupted verification pending.
- **Canonical artifacts untouched:** `experiments/*.json` (match HEAD), `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` inputs.
- **Stale-handoff audit:** the prior durable handoff `HANDOFF_2026-11-23T16-21-41Z_INITIAL_TASK.md` reported HEAD `1e618988` and is now superseded by `6aa51efd`. The 16:24:30Z checkpoint commit repointed only the 80 root-level generic aliases to that stale file; the mirror-dir generic aliases (`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`) still pointed at `handoff_2026-11-23T14-28-00Z_INITIAL_TASK.md`. This refresh repoints every generic alias to this file and leaves historical timestamped artifacts untouched.
- **Note:** this file was created at explicit user request to leave a timestamped, clear initial task message for the next agentic work session. Per the E652–E726 ledger diagnosis, do **not** manufacture further handoff refreshes as a substitute for real work.

## Initial task for the next session

**Default: await explicit user instructions.** Do not invent new experiments, run the verification suite unprompted, change pre-registered gates/outcomes, or modify golden/baseline/canonical artifacts without explicit direction. If you have no explicit instruction, verifying state and stopping is a complete outcome.

If you must act autonomously, work in order:

1. Verify and stop: `git status --porcelain` and `git rev-list --left-right --count origin/main...HEAD`. Report clean/aligned and stop.
2. Reproduce (real work): `pip install -r requirements.txt` if needed, then `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift precisely. Do **not** re-pin artifacts to make tolerance violations disappear.
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

- **Durable artifact (this session):** `HANDOFF_2026-11-23T16-27-17Z_INITIAL_TASK.md` (repo root). All generic aliases across root and mirror dirs (`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`) repointed to it; historical timestamped artifacts left untouched.
- **Supersedes operationally:** `HANDOFF_2026-11-23T16-21-41Z_INITIAL_TASK.md` (stale HEAD reference) and the mirror-dir aliases that still pointed at `handoff_2026-11-23T14-28-00Z_INITIAL_TASK.md`.
- This session created only this durable handoff (and repointed generic aliases). No code, experiments, ledgers, baselines, or canonical artifacts modified. No commit made — left uncommitted pending explicit direction.

(End of file - total 56 lines)