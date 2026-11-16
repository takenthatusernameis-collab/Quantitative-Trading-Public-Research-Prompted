# Agentic Work Session Handoff

**Timestamp**: 2026-11-16T12:34:29Z (UTC)
**Project**: Quantitative-Trading-Public-Research-Prompted
**Branch**: `main` (HEAD `8385f1ac`)
**Session state at handoff**: No active implementation/research task. Fast integrity gate re-run and passing this session (see verified state below).
**Supersedes**: `handoff/handoff_2026-11-16T12-33-03Z_INITIAL_TASK.md` (that file's recorded HEAD `82c96802` is stale; current HEAD is `8385f1ac`).

---

## INITIAL TASK MESSAGE (for the next agentic work session)

**Primary task:** Maintain baseline integrity and reproducibility. Do NOT start new research/experiments unless explicitly requested.

1. **Read context first:** `AGENTS.md`, this handoff, and `ledger/RESEARCH_LEDGER.md` as needed. Check coordination context (`board_read`) for any pending coordinator/peer task before acting.
2. **Fast integrity gate (required before other work):** `SEED=42 bash scripts/check.sh` (or `make check`). Fix any failures before proceeding.
3. **If deeper verification is requested:** `SEED=42 python3 run_all_verification.py` for quick, add `--extended` or `--full` as needed. **Never leave a verification run half-finished.**
4. **If verification was interrupted / baseline looks dirty:** if `.verify_snapshot/` exists, `experiments/*.json` differ unexpectedly from HEAD, or checks report stale snapshot/golden mismatch, recover first: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md` and `ledger/golden_baseline.json` rules). Do **not** commit verification output or re-pin goldens as a side effect of a run.
5. **If no task is posted:** remain in maintenance mode (integrity checks, documentation hygiene consistent with conventions). Research phase is complete (E001–E043); follow pre-registration, promotion-gate, and negative-result recording conventions for any new work.

---

## Project Status

- **Research phase**: Complete (E001–E043). Validated findings in `ledger/RESEARCH_LEDGER.md`.
- **Canonical baseline**: `experiments/*.json` goldens; pinned hashes in `ledger/golden_baseline.json`.
- **CI**: Workflow template only (`.github/workflow-templates/verification-gate.yml`); a maintainer must create the actual workflow via the GitHub UI (automated agents cannot).

## Last verified / known state

- `SEED=42 bash scripts/check.sh` → **ALL checks passed** (exit 0, 2026-11-16T12:34Z), including golden/baseline/data-coverage/JSON-artifact checks and portfolio-opt determinism tests.
- No `.verify_snapshot/` directory present at 2026-11-16T12:34Z.
- `git status` for `experiments/` is clean (no golden drift). Working tree otherwise shows only modified `__pycache__/*.pyc` artifacts (not source changes); re-check at session start.

## Key constraints / reminders

- **Always `SEED=42`** for verification/repro runs. Primary convention: close-to-close v1.2.3.
- **Golden artifacts**: `experiments/*.json` are canonical; verification overwrites then restores — never leave half-finished. Never commit captured verification output.
- **Do not re-pin** E041/E042 grid artifacts to silence known ill-conditioned QP 1-ulp drift (ledger E049 open item).
- Cache/data coverage is enforced (`QUANT_RESEARCH_OFFLINE=1` during verification; pinned vintages/snapshots per `data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`).

## Useful commands

```bash
SEED=42 bash scripts/check.sh          # fast offline gate
make verify-quick                      # ~8 min
make verify-extended                   # ~21 min
make verify-full                       # ~15 min
SEED=42 python3 run_all_verification.py --restore-only
```

*Durable handoff for next agentic session. Update if material state changes.*