# Handoff — Initial Task Message

**Generated:** 2026-11-24T10:57:10Z
**Session:** 2026-11-24T10:57:10Z
**Repo:** Quantitative-Trading-Public-Research-Public-Research
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## Purpose

Durable handoff message for the next agentic work session. Read this first before touching the codebase.

---

## Project context (from AGENTS.md)

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

- `experiments/*.json` are committed golden artifacts. Verification suite overwrites them during a run and restores afterwards — **never leave a verification run half-finished**.
- Seed always `SEED=42`. Suite runs offline via `QUANT_RESEARCH_OFFLINE=1`.
- `python3 -m py_compile` on changed files (no separate linter).
- Do not commit unless explicitly asked.

---

## Quick start commands

```bash
# Convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Verify-convention-only
SEED=42 python3 verify_convention_robustness.py

# Individual drivers
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
```

---

## Clear initial task for next session

There is no pre-defined task queued in this handoff. The next session should:

1. **Confirm scope** — ask the user what they want to work on, or pick up the most recent open item from `ledger/RESEARCH_LEDGER.md` / open issues.
2. **Establish a clean baseline** — run `SEED=42 bash scripts/check.sh` and confirm it passes before making changes.
3. **Work iteratively** — break the task into steps, implement, then run `python3 -m py_compile` on changed files and re-run `scripts/check.sh`.
4. **Never commit** unless the user explicitly requests it.
5. **Leave a new HANDOFF** at the end of the session (timestamped `HANDOFF_<ts>_INITIAL_TASK.md`) summarizing what was done, what's blocked, and the next task.

---

## Key files / locations

- `AGENTS.md` — project commands, conventions, baseline integrity rules
- `ledger/RESEARCH_LEDGER.md` — validated strategies, dispositions (REJECTED / PARTIAL)
- `experiments/` — committed golden experiment artifacts (do not modify directly)
- `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- `src/batch_run.py`, `src/validate.py`, `src/portfolio_opt.py`
- `.verify_snapshot/` — gitignored, holds backup during live verification runs

---

## Standing reminders

- A verification run must never be left half-finished; interrupted runs leave driver output in `experiments/` instead of goldens — recover with `SEED=42 python3 run_all_verification.py --restore-only`.
- Replacing a golden requires re-pinning (`python3 scripts/check_golden_baseline.py --update`) and recording in the ledger first.
- Do not commit verification output as a side effect of running the suite.

---

End of handoff.