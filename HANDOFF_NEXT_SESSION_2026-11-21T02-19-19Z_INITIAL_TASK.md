# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-21T02:19:19Z
**Prepared by:** session at HEAD `17812cba` (handoff refresh only; no research performed)
**Repository HEAD at creation:** `17812cba1962f6c27f71cacff0a6a95180eb1623` (`chore(kilo): checkpoint agent session`)
**Branch:** `main` (HEAD == `origin/main`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial Task Message (read this first)

> You are starting a fresh agentic work session in this repository. Orient
> yourself and confirm the canonical baselines are intact. Do **not** start new
> research, re-pin goldens/data, run the verification suite, or commit anything
> until the user gives an explicit task. The research phase is closed (E001–E043).
> When you finish, leave your own timestamped handoff using the procedure at the bottom.

## Start-Here Checklist (in order)

1. **Orient.** Run `git log --oneline -3` and `git status --porcelain`. Read `AGENTS.md`
   and the tail of `ledger/RESEARCH_LEDGER.md`. Confirm `git rev-parse HEAD origin/main` agree.
2. **Recover any interrupted verification.** If `.verify_snapshot/` exists or
   `experiments/*.json` differ from HEAD, run
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`)
   before anything else.
3. **Confirm both golden guards pass** (fast, offline):
   - `python3 scripts/check_goldens_clean.py` -> "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD"
   - `python3 scripts/check_golden_baseline.py` -> "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT"
4. **Provision dependencies if needed:** `pip install -r requirements.txt`
5. **Run the fast gate:** `SEED=42 bash scripts/check.sh` (or `make check`).
6. **Do the user's task, or stop.** Do not invent scope from this handoff.
7. **Leave your own handoff** at the end (see *Handoff Procedure*).

## Verification Scopes (only if the user asks to verify)

```bash
SEED=42 bash scripts/check.sh                     # fast convention/guard gate (~seconds)
SEED=42 python3 run_all_verification.py           # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # +18 drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --full    # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 verify_convention_robustness.py   # reads JSONs, no writes
```

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Default: await explicit user instructions; do not invent scope.
